import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[1]
CHART = ROOT / "charts/cloud-visi"


def render(*args):
    result = subprocess.run(["helm", "template", "cloud-visi", str(CHART), "--namespace", "cloud-visi", *args], text=True, capture_output=True)
    if result.returncode:
        raise AssertionError(result.stderr)
    return [doc for doc in yaml.safe_load_all(result.stdout) if doc]


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ChartTests(unittest.TestCase):
    def test_single_writer_and_private_access(self):
        docs = render()
        app = next(d for d in docs if d["kind"] == "Deployment")
        self.assertEqual(app["spec"]["replicas"], 1)
        self.assertEqual(app["spec"]["strategy"]["type"], "Recreate")
        pod = app["spec"]["template"]["spec"]
        self.assertFalse(pod["automountServiceAccountToken"])
        self.assertTrue(pod["securityContext"]["runAsNonRoot"])
        container = pod["containers"][0]
        self.assertEqual(container["readinessProbe"]["httpGet"]["path"], "/readyz")
        self.assertEqual(container["livenessProbe"]["httpGet"]["path"], "/healthz")
        self.assertFalse(any(d["kind"] in ("Ingress", "Secret", "ClusterRole") for d in docs))
        self.assertTrue(all(d["spec"].get("type", "ClusterIP") == "ClusterIP" for d in docs if d["kind"] == "Service"))

    def test_upgrade_keeps_storage_and_uses_existing_secrets(self):
        docs = render()
        pvcs = [d for d in docs if d["kind"] == "PersistentVolumeClaim"]
        self.assertEqual(len(pvcs), 2)
        self.assertTrue(all(p["metadata"]["annotations"]["helm.sh/resource-policy"] == "keep" for p in pvcs))
        app = next(d for d in docs if d["kind"] == "Deployment")
        env = app["spec"]["template"]["spec"]["containers"][0]["env"]
        for name in ("DATABASE_URL", "SECRET_KEY"):
            ref = next(e for e in env if e["name"] == name)["valueFrom"]["secretKeyRef"]
            self.assertEqual(ref, {"name": "cloud-visi-secrets", "key": name})

    def test_external_database_and_existing_repository_claim(self):
        docs = render("-f", str(ROOT / "examples/values-external-postgres.yaml"), "--set", "persistence.existingClaim=kept-repositories")
        self.assertFalse(any(d["kind"] in ("StatefulSet", "PersistentVolumeClaim") for d in docs))
        app = next(d for d in docs if d["kind"] == "Deployment")
        volume = app["spec"]["template"]["spec"]["volumes"][0]
        self.assertEqual(volume["persistentVolumeClaim"]["claimName"], "kept-repositories")

    def test_digest_takes_precedence(self):
        digest = "sha256:" + "a" * 64
        app = next(d for d in render("--set", "image.digest=" + digest, "--set", "image.tag=ignored") if d["kind"] == "Deployment")
        self.assertEqual(app["spec"]["template"]["spec"]["containers"][0]["image"], "ghcr.io/cloud-visi/cloud-visi@" + digest)

    def test_unsafe_or_incomplete_configuration_is_rejected(self):
        for setting in ("replicaCount=2", "secrets.existingSecret=", "ingress.enabled=true", "image.digest=not-a-digest"):
            with self.subTest(setting=setting):
                result = subprocess.run(["helm", "template", "cloud-visi", str(CHART), "--set", setting], capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)

    def test_trial_mount_is_optional_and_read_only(self):
        default = next(d for d in render() if d["kind"] == "Deployment")
        self.assertFalse(any(v["name"] == "trial-license" for v in default["spec"]["template"]["spec"]["volumes"]))
        app = next(d for d in render("--set", "trial.existingSecret=partner-trial") if d["kind"] == "Deployment")
        pod = app["spec"]["template"]["spec"]
        volume = next(v for v in pod["volumes"] if v["name"] == "trial-license")
        self.assertEqual(volume["secret"], {"secretName": "partner-trial", "defaultMode": 0o440, "items": [{"key": "trial-key", "path": "license"}]})
        container = pod["containers"][0]
        mount = next(m for m in container["volumeMounts"] if m["name"] == "trial-license")
        self.assertTrue(mount["readOnly"])
        self.assertEqual(next(e for e in container["env"] if e["name"] == "TRIAL_LICENSE_FILE")["value"], "/etc/cloud-visi/trial/license")
        invalid = subprocess.run(["helm", "template", "cloud-visi", str(CHART), "--set", "trial.existingSecret=trial", "--set", "trial.key="], capture_output=True)
        self.assertNotEqual(invalid.returncode, 0)

    def test_ingress_can_use_existing_authentication_gateway(self):
        docs = render("--set", "ingress.enabled=true", "--set", "ingress.authenticationConfirmed=true", "--set", "ingress.host=cloud-visi.example.com")
        ingress = next(d for d in docs if d["kind"] == "Ingress")
        self.assertEqual(ingress["spec"]["rules"][0]["host"], "cloud-visi.example.com")


class CredentialTests(unittest.TestCase):
    def test_compose_credentials_are_private_and_preserved(self):
        module = load_script("create-compose-env")
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()) as output:
            path = Path(directory) / ".env"
            self.assertTrue(module.create(path))
            first = path.read_bytes()
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertFalse(module.create(path))
            self.assertEqual(path.read_bytes(), first)
            for line in first.decode().splitlines():
                if line.startswith(("SECRET_KEY=", "POSTGRES_PASSWORD=")):
                    self.assertNotIn(line.split("=", 1)[1], output.getvalue())

    def test_existing_kubernetes_secret_is_never_replaced(self):
        module = load_script("create-kubernetes-secret")
        args = SimpleNamespace(context="local", namespace="cloud-visi", name="cloud-visi-secrets")
        with patch.object(module.subprocess, "run", return_value=SimpleNamespace(returncode=0, stdout="secret/cloud-visi-secrets")) as run, contextlib.redirect_stdout(io.StringIO()):
            module.create(args)
            self.assertEqual(run.call_count, 1)

    def test_kubernetes_secret_is_created_from_stdin_without_logging_values(self):
        module = load_script("create-kubernetes-secret")
        args = SimpleNamespace(context="local", namespace="cloud-visi", name="cloud-visi-secrets", external_database=False, database_host=None, release="cloud-visi")
        with patch.object(module.subprocess, "run", side_effect=[SimpleNamespace(returncode=0, stdout=""), SimpleNamespace(returncode=0)]) as run, contextlib.redirect_stdout(io.StringIO()) as output:
            module.create(args)
            call = run.call_args_list[-1]
            self.assertEqual(call.args[0][-3:], ["create", "-f", "-"])
            data = json.loads(call.kwargs["input"])["stringData"]
            self.assertIn("cloud-visi-postgres:5432", data["DATABASE_URL"])
            self.assertEqual(len(data["SECRET_KEY"]), 64)
            self.assertNotIn(data["SECRET_KEY"], output.getvalue())
            self.assertNotIn(data["POSTGRES_PASSWORD"], output.getvalue())


class DocumentationTests(unittest.TestCase):
    def test_no_em_dashes_or_private_product_files(self):
        for path in ROOT.rglob("*.md"):
            self.assertNotIn(chr(0x2014), path.read_text(), str(path))
        for path in ROOT.rglob("*"):
            if path.is_file() and ".git" not in path.parts:
                self.assertNotEqual(path.suffix, ".go", str(path))
                self.assertNotIn(path.name, (".env", "CLAUDE.md", "CONTRACT.md", "PROGRESS.md"))

    def test_partner_feedback_has_no_prescribed_outcomes(self):
        text = (ROOT / "docs/feedback.md").read_text().lower()
        self.assertNotIn("expected results", text)
        self.assertIn("no required task list", text)

    def test_trial_compose_overlay_keeps_data_and_refuses_missing_file(self):
        overlay = yaml.safe_load((ROOT / "compose.trial.yaml").read_text())
        self.assertEqual(set(overlay["services"]), {"app"})
        app = overlay["services"]["app"]
        self.assertEqual(app["environment"], {"TRIAL_LICENSE_FILE": "/etc/cloud-visi/trial/license"})
        mount = app["volumes"][0]
        self.assertTrue(mount["read_only"])
        self.assertFalse(mount["bind"]["create_host_path"])
        self.assertIn("TRIAL_LICENSE_PATH:?", mount["source"])
        self.assertNotIn("volumes", overlay)

    def test_compose_pulls_image_and_exposes_only_localhost(self):
        services = yaml.safe_load((ROOT / "compose.yaml").read_text())["services"]
        self.assertNotIn("build", services["app"])
        self.assertEqual(services["app"]["ports"], ["127.0.0.1:8080:8080"])
        self.assertNotIn("ports", services["postgres"])


if __name__ == "__main__":
    unittest.main()
