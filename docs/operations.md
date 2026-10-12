# Keep or remove your installation

## Restart

A restart should keep the existing database, repository volume, and encryption key.

For Kubernetes:

```bash
kubectl --context "$CONTEXT" -n cloud-visi rollout restart deployment/cloud-visi
kubectl --context "$CONTEXT" -n cloud-visi rollout status deployment/cloud-visi --timeout=5m
```

For Compose, use `docker compose restart app`.

## Upgrade

Read the release notes and make a backup first. Keep the same installation Secret or Compose `.env` file. Use the Helm install command with the new chart version, or select the new Compose image as described in [Compose setup](compose.md).

The application runs one instance. An upgrade stops the old instance before starting the new one, so there is a short interruption. Migrations finish before it accepts requests. Do not run a second installation against the same database.

A Helm rollback changes the application deployment, not the database schema. Use it only when the release notes confirm compatibility with the schema already installed. Do not assume an old image can read a newer database.

## Back up

A recoverable backup needs the database and its original encryption key. The repository volume holds local copies and should be retained during normal upgrades. Repository copies can be fetched again; the database and key cannot be reconstructed that way.

For the bundled Kubernetes database:

```bash
umask 077
mkdir -p backup
kubectl --context "$CONTEXT" -n cloud-visi exec cloud-visi-postgres-0 --   sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' > backup/database.dump
kubectl --context "$CONTEXT" -n cloud-visi get secret cloud-visi-secrets -o json > backup/installation-secret.json
```

Keep these files in private, protected storage. The Secret backup contains credentials. Do not commit it or share it in an issue.

For Compose, preserve `.env` in protected storage and make a database dump:

```bash
umask 077
mkdir -p backup
docker compose exec -T postgres sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' > backup/database.dump
```

For an external database, use your platform's PostgreSQL backup process and preserve the application encryption key separately.

## Restore

Restore into a new, empty PostgreSQL 16 database with UTF8 and ICU support. Keep the existing installation stopped while switching its database connection.

1. Restore the dump with `pg_restore --exit-on-error` using your database access method. Do not restore over an active application database.
2. Restore the original encryption key from the matching Secret backup or `.env` backup.
3. Set the database connection to the restored database without printing it or placing it in Git.
4. Start one application instance and check readiness and your saved connections.

Keep the old database until you have checked the restored installation. Your platform team can help with the database connection and secure Secret handling.

## Remove the application while keeping data

```bash
helm uninstall cloud-visi --kube-context "$CONTEXT" --namespace cloud-visi
```

The chart marks its database and repository claims to be kept. The installation Secret is created separately and is also kept. Do not delete the namespace if you want these to remain. To reinstall using the default claim names, keep the same installation Secret and
select the announced chart version:

```bash
helm upgrade --install cloud-visi oci://ghcr.io/cloud-visi/charts/cloud-visi \
  --version "$CHART_VERSION" --kube-context "$CONTEXT" --namespace cloud-visi \
  --set persistence.existingClaim=cloud-visi-repositories \
  --set postgresql.storage.existingClaim=cloud-visi-database \
  --wait --timeout 10m
```

If you used custom claim or Secret names, supply those original names instead.
For an external database, also keep `postgresql.enabled=false` and its original
connection settings.

For Compose:

```bash
docker compose down
```

This keeps named volumes. Keep `.env` too.

## Delete data deliberately

Only do this when you want to discard the installation and have saved anything you need.

For Kubernetes, uninstall the chart, then explicitly delete the two claims and the installation Secret in the correct context and namespace. Deleting a claim can cause the storage provider to delete its underlying disk. Never delete a claim used by an external database.

For Compose, `docker compose down --volumes` deletes the application volumes. Removing `.env` also removes the saved encryption key. These are separate actions from a normal stop or upgrade.
