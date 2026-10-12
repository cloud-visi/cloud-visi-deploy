# Troubleshooting

## The image cannot be downloaded

Check that the image version or digest matches the beta release page and your cluster can reach `ghcr.io`. The OCI chart is not published yet; use the local chart files. Public images do not need a registry token.

## Helm waits or a pod keeps restarting

```bash
kubectl --context "$CONTEXT" -n cloud-visi get pods,pvc
kubectl --context "$CONTEXT" -n cloud-visi get events --sort-by=.lastTimestamp
```

A pending volume usually means no suitable storage class is available. A missing Secret means step 3 of the install guide did not finish or the configured Secret name differs.

Database initialisation and application migrations run before the application is ready. Readiness can also fail when PostgreSQL is unavailable. Liveness does not use database availability to trigger restarts.

You can inspect logs locally:

```bash
kubectl --context "$CONTEXT" -n cloud-visi logs deployment/cloud-visi --tail=100
```

Do not paste unredacted logs into public issues.

## The page does not open

Keep the port-forward terminal running. Check that its local port matches the address in your browser. If another program is using port 8080, forward `8081:8080` instead.

## A repository is not listed

Check the organization or owner, project, token permissions, repository selection on the token, and any organization approval requirement. A token can discover only repositories it can access. Start with a repository containing Terraform `.tf` files.

## State is unavailable

State access is optional and separate from code access. Check whether the Terraform project declares a supported backend, whether the server can reach the storage endpoint, and whether its identity has read access to the state file. Repository settings explain the checks that could not complete.

## Saved credentials cannot be read after an upgrade

Check that the installation still uses its original `SECRET_KEY`. Restoring a database without the original key does not restore usable credentials. Restore the matching key or enter the affected connection credentials again.

## Compose does not start

Run `python3 scripts/create-compose-env.py` if `.env` does not exist. Check Docker Desktop is running in Linux container mode. Use `docker compose ps` to inspect status. Do not run commands that print resolved environment values when sharing diagnostics.
