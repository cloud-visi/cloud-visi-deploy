#!/usr/bin/env python3
"""Create a stable installation Secret. Never print its values or replace an existing Secret."""
import argparse
import getpass
import json
import secrets
import subprocess


def create(args):
    base = ["kubectl", "--context", args.context, "-n", args.namespace]
    check = subprocess.run(base + ["get", "secret", args.name, "--ignore-not-found", "-o", "name"], capture_output=True, text=True)
    if check.returncode:
        raise SystemExit("Cannot check for an existing Secret. Check your Kubernetes context and namespace.")
    if check.stdout.strip():
        print("Existing Secret kept. No credentials were changed.")
        return
    password = secrets.token_hex(32)
    data = {"SECRET_KEY": secrets.token_hex(32)}
    if args.external_database:
        url = getpass.getpass("Database connection URL (hidden): ")
        if not url.startswith(("postgres://", "postgresql://")):
            raise SystemExit("Use a PostgreSQL connection URL.")
        data["DATABASE_URL"] = url
    else:
        data.update(POSTGRES_USER="infra_timeline", POSTGRES_DB="infra_timeline", POSTGRES_PASSWORD=password)
        host = args.database_host or args.release + "-postgres"
        data["DATABASE_URL"] = "postgres://infra_timeline:" + password + "@" + host + ":5432/infra_timeline?sslmode=disable"
    manifest = {"apiVersion": "v1", "kind": "Secret", "metadata": {"name": args.name, "namespace": args.namespace}, "type": "Opaque", "stringData": data}
    result = subprocess.run(base + ["create", "-f", "-"], input=json.dumps(manifest), capture_output=True, text=True)
    if result.returncode:
        raise SystemExit("Secret creation failed. Check permissions and whether another install created it. No existing Secret was replaced.")
    print("Installation Secret created. Keep it for upgrades and recovery.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--context", required=True)
    parser.add_argument("--namespace", default="cloud-visi")
    parser.add_argument("--name", default="cloud-visi-secrets")
    parser.add_argument("--release", default="cloud-visi")
    parser.add_argument("--database-host")
    parser.add_argument("--external-database", action="store_true")
    create(parser.parse_args())
