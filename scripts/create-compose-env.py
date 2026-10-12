#!/usr/bin/env python3
"""Create local credentials without displaying them or replacing an existing file."""
import argparse
import os
from pathlib import Path
import secrets


def create(path):
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        print("Existing credentials kept. No file was changed.")
        return False
    with os.fdopen(fd, "w") as output:
        output.write("POSTGRES_USER=infra_timeline\nPOSTGRES_DB=infra_timeline\n")
        output.write("POSTGRES_PASSWORD=" + secrets.token_hex(32) + "\n")
        output.write("SECRET_KEY=" + secrets.token_hex(32) + "\n")
    print("Credentials saved locally. Keep this file for restarts and upgrades.")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(".env"))
    create(parser.parse_args().output)
