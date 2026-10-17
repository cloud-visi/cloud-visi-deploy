# Optional Docker Compose setup

This is an optional deployment path. The authenticated beta requires an existing trusted HTTPS proxy; Compose does not provision TLS.

Use the versioned beta image from the release page.

## What you need

Docker in Linux container mode, Git, Python 3, and an existing trusted TLS proxy with a hostname you control. Docker Compose is included with Docker Desktop.

## Install

```bash
git clone https://github.com/cloud-visi/cloud-visi-deploy.git
cd cloud-visi-deploy
python3 scripts/create-compose-env.py
export AUTH_PUBLIC_URL=https://your-cloud-visi-hostname.example
CLOUD_VISI_IMAGE=ghcr.io/cloud-visi/cloud-visi:0.1.0-beta.2 docker compose pull
CLOUD_VISI_IMAGE=ghcr.io/cloud-visi/cloud-visi:0.1.0-beta.2 docker compose up -d --wait --wait-timeout 600
```

The script creates a local `.env` file with a database password and an encryption key. It does not print either value. Running it again keeps the existing file.

Route your existing HTTPS proxy to the loopback backend at 127.0.0.1:8080 and preserve the public Host and Origin. Complete [administrator bootstrap](access-control.md), sign in at your configured HTTPS origin, then [activate the trial](trial.md) and [connect a repository](connect-repositories.md). No local image build is needed. Store the non-secret AUTH_PUBLIC_URL in your local .env for later restarts.

If port 8080 is already in use, stop the process you no longer need or change the left-hand port in `compose.yaml` to `127.0.0.1:8081:8080`. Then run `docker compose up -d` and update the existing proxy upstream to that port. Continue visiting the configured HTTPS origin.

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
