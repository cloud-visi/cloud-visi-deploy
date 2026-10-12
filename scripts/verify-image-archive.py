#!/usr/bin/env python3
"""Verify a locally built beta OCI archive before publishing its runtime images."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import tarfile

SOURCE = "https://github.com/cloud-visi/cloud-visi-deploy"


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def verify(path, expected_sha, expected_digest, version, revision):
    require(re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+-beta\.[0-9]+", version), "Only versioned beta images are allowed")
    checksum = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            checksum.update(chunk)
    require(checksum.hexdigest() == expected_sha, "Archive checksum does not match approval")
    with tarfile.open(path) as archive:
        names = set()
        for member in archive:
            name = member.name.rstrip("/")
            require(name not in names, "Duplicate archive member")
            names.add(name)
            require(member.isfile() or member.isdir(), "Archive contains a link or special file")
            require(name in ("oci-layout", "index.json", "blobs", "blobs/sha256") or re.fullmatch(r"blobs/sha256/[a-f0-9]{64}", name), "Unexpected archive path")
            if member.isfile() and name.startswith("blobs/"):
                data = archive.extractfile(member).read()
                require(hashlib.sha256(data).hexdigest() == name.rsplit("/", 1)[1], "Blob digest mismatch")

        def blob(digest):
            require(re.fullmatch(r"sha256:[a-f0-9]{64}", digest), "Invalid blob digest")
            return archive.extractfile("blobs/sha256/" + digest.split(":")[1])

        def document(digest):
            return json.load(blob(digest))

        index = json.load(archive.extractfile("index.json"))
        require(len(index["manifests"]) == 1 and index["manifests"][0]["digest"] == expected_digest, "Image index differs from approval")
        root = document(expected_digest)
        platforms = []
        evidence = {}
        for descriptor in root["manifests"]:
            manifest = document(descriptor["digest"])
            platform = descriptor.get("platform", {})
            if platform.get("os") == "linux":
                arch = platform["architecture"]
                platforms.append(arch)
                config = document(manifest["config"]["digest"])
                require(config["os"] == "linux" and config["architecture"] == arch, "Architecture mismatch")
                runtime = config["config"]
                labels = runtime.get("Labels", {})
                require(runtime.get("User") == "10001:10001", "Application must run as user 10001")
                require(labels.get("org.opencontainers.image.source") == SOURCE, "Image source label must name the deployment repository")
                require(labels.get("org.opencontainers.image.version") == version and labels.get("org.opencontainers.image.revision") == revision, "Version or revision mismatch")
                for layer in manifest["layers"]:
                    with tarfile.open(fileobj=blob(layer["digest"]), mode="r|*") as files:
                        for entry in files:
                            parts = PurePosixPath(entry.name).parts
                            require(".git" not in parts and "src" not in parts, "Image contains a source checkout")
                            require(not any(p.startswith(".env") for p in parts), "Image contains environment files")
                            require(not entry.name.endswith(".go") and PurePosixPath(entry.name).name not in ("go.mod", "go.sum"), "Image contains product source files")
            else:
                require(descriptor.get("annotations", {}).get("vnd.docker.reference.type") == "attestation-manifest", "Unexpected non-runtime manifest")
                subject = descriptor["annotations"]["vnd.docker.reference.digest"]
                evidence[subject] = {document(layer["digest"]).get("predicateType") for layer in manifest["layers"]}
        require(sorted(platforms) == ["amd64", "arm64"], "Exactly AMD64 and ARM64 runtime images are required")
        for descriptor in root["manifests"]:
            if descriptor.get("platform", {}).get("os") == "linux":
                predicates = evidence.get(descriptor["digest"], set())
                require("https://spdx.dev/Document" in predicates and bool(predicates & {"https://slsa.dev/provenance/v0.2", "https://slsa.dev/provenance/v1"}), "Each runtime image needs SBOM and provenance")
        print("Verified beta archive: AMD64, ARM64, non-root runtime, SBOMs, provenance and no source checkout")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--record", type=Path, required=True)
    args = parser.parse_args()
    record = json.loads(args.record.read_text())
    verify(args.archive, record["archive_sha256"], record["image_digest"], record["version"], record["source_revision"])
