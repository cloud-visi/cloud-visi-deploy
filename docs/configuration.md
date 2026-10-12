# Configuration reference

Most connection settings are entered in the application. Helm values configure how it runs.

| Helm value | Purpose |
| --- | --- |
| `image.repository`, `image.tag`, `image.digest` | Choose the release image. A digest takes precedence over a tag. |
| `secrets.existingSecret` | Secret holding `DATABASE_URL` and `SECRET_KEY`. Bundled PostgreSQL also needs `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB`. |
| `postgresql.enabled` | Use bundled PostgreSQL or your own database. |
| `persistence.*` | Repository volume size, storage class, or an existing claim. |
| `postgresql.storage.*` | Database volume size, storage class, or an existing claim. |
| `resources`, `postgresql.resources` | CPU and memory requests and limits. |
| `config.pollInterval` | How often to read new information. Default: `5m`. |
| `config.backfillDays` | First-sync history lookback. Default: `30`. |
| `nodeSelector`, `tolerations`, `affinity` | Pod scheduling preferences. |
| `serviceAccount.annotations`, `extraEnv`, `extraVolumes`, `extraVolumeMounts` | Connect an existing workload identity or mount read-only credentials. Use secret references, not secret values in values files. |
| `ingress.*` | Optional access through an existing authentication gateway. Disabled by default. |

One application replica is required. The chart rejects higher replica counts. Do not attach another Cloud-Visi installation to the same database or repository volume.

The application runs as UID/GID 10001. Existing repository volumes must be writable by this user. AWS profile mounts belong at `/home/cloudvisi/.aws` and must be readable by this user. Mount only the dedicated credentials you need, read-only.

The chart does not regenerate credentials during an upgrade. Keep the same Secret. If you change the release name or `fullnameOverride`, check the database hostname in `DATABASE_URL`; the bundled database service is named `<application-name>-postgres`.

TLS for an external database and a private connection to its host are managed by your platform team. PostgreSQL 16, UTF8 encoding, and ICU Unicode collation support are required for the initial tested profile.

Shared UI access requires authentication in front of Cloud-Visi. Setting `ingress.authenticationConfirmed=true` only records that you have configured it; it does not add authentication.
