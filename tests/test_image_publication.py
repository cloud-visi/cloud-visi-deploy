import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("verify_image_archive", ROOT / "scripts/verify-image-archive.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
VERSION = "0.1.0-beta.1"
REVISION = "a" * 40


def fixture(path, platforms=("amd64", "arm64"), user="10001:10001", source_file=False, provenance="https://slsa.dev/provenance/v1", attest=True):
    blobs = {}

    def blob(data):
        if not isinstance(data, bytes):
            data = json.dumps(data).encode()
        digest = hashlib.sha256(data).hexdigest()
        blobs["blobs/sha256/" + digest] = data
        return {"digest": "sha256:" + digest, "size": len(data)}

    layer = io.BytesIO()
    with tarfile.open(fileobj=layer, mode="w:gz") as tar:
        data = b"example runtime file"
        info = tarfile.TarInfo("src/private.go" if source_file else "server")
        info.size = len(data)
        tar.addfile(info, io.BytesIO(data))
    layer_desc = blob(layer.getvalue())
    manifests = []
    for arch in platforms:
        config = blob({"os": "linux", "architecture": arch, "config": {"User": user, "Labels": {"org.opencontainers.image.source": module.SOURCE, "org.opencontainers.image.version": VERSION, "org.opencontainers.image.revision": REVISION}}})
        runtime = blob({"config": config, "layers": [layer_desc]})
        runtime["platform"] = {"os": "linux", "architecture": arch}
        manifests.append(runtime)
        if attest:
            evidence = blob({"layers": [blob({"predicateType": p}) for p in ("https://spdx.dev/Document", provenance)]})
            evidence["platform"] = {"os": "unknown", "architecture": "unknown"}
            evidence["annotations"] = {"vnd.docker.reference.type": "attestation-manifest", "vnd.docker.reference.digest": runtime["digest"]}
            manifests.append(evidence)
    root = blob({"manifests": manifests})
    files = {"oci-layout": b'{"imageLayoutVersion":"1.0.0"}', "index.json": json.dumps({"manifests": [root]}).encode(), **blobs}
    with tarfile.open(path, "w") as tar:
        for name, data in files.items():
            info = tarfile.TarInfo(name)
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))
    return hashlib.sha256(path.read_bytes()).hexdigest(), root["digest"]


class ImagePublicationTests(unittest.TestCase):
    def verify_fixture(self, **kwargs):
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()):
            path = Path(directory) / "image.tar"
            sha, digest = fixture(path, **kwargs)
            module.verify(path, sha, digest, VERSION, REVISION)

    def test_both_supported_provenance_formats(self):
        for p in ("https://slsa.dev/provenance/v0.2", "https://slsa.dev/provenance/v1"):
            self.verify_fixture(provenance=p)

    def test_rejects_private_source_in_runtime(self):
        with self.assertRaisesRegex(ValueError, "source checkout"):
            self.verify_fixture(source_file=True)

    def test_rejects_missing_target_architecture(self):
        with self.assertRaisesRegex(ValueError, "AMD64 and ARM64"):
            self.verify_fixture(platforms=("arm64",))

    def test_rejects_root_runtime(self):
        with self.assertRaisesRegex(ValueError, "user 10001"):
            self.verify_fixture(user="0")

    def test_rejects_missing_attestations(self):
        with self.assertRaisesRegex(ValueError, "SBOM and provenance"):
            self.verify_fixture(attest=False)

    def test_rejects_modified_archive_and_wrong_approved_digest(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "image.tar"
            sha, digest = fixture(path)
            with self.assertRaisesRegex(ValueError, "checksum"):
                module.verify(path, "0" * 64, digest, VERSION, REVISION)
            with self.assertRaisesRegex(ValueError, "differs from approval"):
                module.verify(path, sha, "sha256:" + "0" * 64, VERSION, REVISION)

    def test_publisher_has_no_product_checkout_or_chart_push(self):
        text = (ROOT / ".github/workflows/publish-beta-image.yaml").read_text()
        workflow = yaml.safe_load(text)
        triggers = workflow.get("on", workflow.get(True))
        self.assertEqual(triggers["push"]["branches"], ["codex/beta-image-release"])
        self.assertEqual(triggers["push"]["paths"], [".github/workflows/publish-beta-image.yaml"])
        self.assertIn("workflow_dispatch", triggers)
        self.assertEqual(workflow["jobs"]["publish"]["permissions"], {"contents": "read", "packages": "write"})
        for forbidden in ("dev.azure.com", "helm push", "docker build", "git clone"):
            self.assertNotIn(forbidden, text)
        self.assertIn('test "$(oras resolve "$IMAGE:$VERSION")" = "$digest"', text)
        self.assertIn("Refusing to replace it", text)


if __name__ == "__main__":
    unittest.main()
