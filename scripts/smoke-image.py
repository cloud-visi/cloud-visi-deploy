#!/usr/bin/env python3
"""Check the new authenticated beta runtime using disposable container data."""
import argparse
import json
import re
import secrets
import subprocess


def run(container, args, data=None):
    result = subprocess.run(
        ["docker", "exec", "-i", container, *args], input=data,
        text=True, capture_output=True,
    )
    if result.returncode:
        raise RuntimeError("Disposable image verification command failed; credentials omitted")
    return result


def verify(container, record, architecture):
    password = secrets.token_urlsafe(32)
    run(container, ["sh", "-c", "umask 077; cat > /tmp/cloudvisi-smoke-password"], password + "\n")
    try:
        run(container, ["/server", "-auth-admin-bootstrap", "-auth-username", "smoke-admin",
                        "-auth-password-file", "/tmp/cloudvisi-smoke-password"])
        payload = json.dumps({"username": "smoke-admin", "password": password})
        login = run(container, ["sh", "-c",
            "umask 077; cat > /tmp/cloudvisi-smoke-request; "
            "wget -S -q -O - --header='Origin: http://127.0.0.1:8080' "
            "--header='Content-Type: application/json' "
            "--post-file=/tmp/cloudvisi-smoke-request http://127.0.0.1:8080/api/auth/login"], payload)
        session = json.loads(login.stdout)
        assert session["authenticated"] is True
        cookies = re.findall(r"(?im)^\s*Set-Cookie:\s*([^;\r\n]+)", login.stderr)
        assert len(cookies) == 1 and cookies[0].startswith("cloudvisi_dev_session=")

        def get(path):
            reply = run(container, ["wget", "-q", "-O", "-", "--header=Cookie: " + cookies[0],
                                    "http://127.0.0.1:8080" + path])
            return json.loads(reply.stdout)

        version = get("/api/version")
        for field, expected in [("version", record["version"]), ("revision", record["source_revision"]),
                                ("build_time", record["build_time"]), ("os", "linux"), ("arch", architecture)]:
            assert version[field] == expected, "Runtime identity mismatch: " + field
        trial = get("/api/trial")
        assert trial["state"] == "activation_required" and trial["activation_available"] is True
        print("Verified native authenticated runtime:", version["version"], architecture)
        print("Fresh trial requires valid owner activation; no provider credentials or fixtures imported")
        return cookies[0], session["csrf_token"], trial["installation_id"]
    finally:
        run(container, ["rm", "-f", "/tmp/cloudvisi-smoke-password", "/tmp/cloudvisi-smoke-request"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--container", required=True)
    parser.add_argument("--record", required=True)
    parser.add_argument("--arch", required=True, choices=["amd64", "arm64"])
    args = parser.parse_args()
    with open(args.record) as stream:
        verify(args.container, json.load(stream), args.arch)
