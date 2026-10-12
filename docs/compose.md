# Optional Docker Compose setup

This is a local option for Docker Desktop users. Kubernetes with Helm remains the supported deployment path for the preview.

The first image has not been published yet. Use these instructions after the release is announced.

## What you need

Docker Desktop in Linux container mode, Git, and Python 3. Docker Compose is included with Docker Desktop.

## Install

```bash
git clone https://github.com/cloud-visi/cloud-visi-deploy.git
cd cloud-visi-deploy
python3 scripts/create-compose-env.py
docker compose pull
docker compose up -d --wait --wait-timeout 600
```

The script creates a local `.env` file with a database password and an encryption key. It does not print either value. Running it again keeps the existing file.

Open http://127.0.0.1:8080 and [connect a repository](connect-repositories.md). No local image build is needed.

If port 8080 is already in use, stop the process you no longer need or change the left-hand port in `compose.yaml` to `127.0.0.1:8081:8080`. Then run `docker compose up -d` and visit port 8081.

## Stop and start again

```bash
docker compose stop
docker compose start
```

The database and repository volumes stay in place. Keep your `.env` file as well. Losing the encryption key can prevent the application from reading saved credentials.

## Choose a release

Set `CLOUD_VISI_IMAGE` in your local `.env` to the versioned image or digest listed on the release page, then run:

```bash
docker compose pull
docker compose up -d --wait --wait-timeout 600
```

Read the release notes and back up your data before upgrading. Do not use an arbitrary development image for an existing installation.
