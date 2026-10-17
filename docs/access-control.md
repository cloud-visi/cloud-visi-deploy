# Sign-in and repository access

Beta.2 adds local administrator accounts and repository-scoped viewers. Git author
identities do not create application accounts. There is no public registration.

## Configure HTTPS before starting

Set `AUTH_PUBLIC_URL` to the exact HTTPS origin users visit, such as
`https://cloud-visi.example.com`, with no path, query or fragment. Configure your
existing trusted TLS proxy to preserve the public Host and Origin and keep direct
backend access private. Compose and Helm do not create a TLS proxy for you.

For Compose, set `AUTH_PUBLIC_URL` in your local environment or `.env`. For Helm,
set `config.authPublicURL`. Missing or invalid origins refuse application startup.
Sessions use Secure, HttpOnly, SameSite=Strict cookies. Forwarded user headers do
not replace sign-in. Plain HTTP port forwarding is insufficient for browser use.

The explicit loopback HTTP mode is for direct host development. Do not enable it
on a container-wide listener or expose it through a tunnel.

## Create the first administrator

Create an owner-only password file outside the checkout, mode 0600, containing a
password of 12 to 256 characters. Never put a password in command arguments,
environment variables, committed files or shared logs. The following commands
stream its contents without printing them. Replace the example username.

For an existing Compose application:

```bash
docker compose exec -T app sh -c 'umask 077; cat > /tmp/bootstrap-password' < /secure/admin-password
docker compose exec app /server -auth-admin-bootstrap \
  -auth-username installation-admin -auth-password-file /tmp/bootstrap-password
docker compose exec app rm -f /tmp/bootstrap-password
```

For Kubernetes, name the intended context and namespace explicitly:

```bash
CONTEXT=your-context-name
kubectl --context "$CONTEXT" -n cloud-visi exec -i deployment/cloud-visi -- \
  sh -c 'umask 077; cat > /tmp/bootstrap-password' < /secure/admin-password
kubectl --context "$CONTEXT" -n cloud-visi exec deployment/cloud-visi -- \
  /server -auth-admin-bootstrap -auth-username installation-admin \
  -auth-password-file /tmp/bootstrap-password
kubectl --context "$CONTEXT" -n cloud-visi exec deployment/cloud-visi -- \
  rm -f /tmp/bootstrap-password
```

Use the actual deployment name if you installed with another release name.
Bootstrap is available before trial activation and refuses to create another
initial administrator once an account exists. Sign in at the configured HTTPS
origin, activate the installation trial, then configure provider connections.

## Recovery and viewers

The host operator can recover an existing administrator using the same secure
password-file procedure with `-auth-admin-reset` instead of bootstrap. Recovery
retains the account ID, revokes its sessions and never promotes a viewer.

Administrators can manage accounts and repository grants in Manage access.
Viewers can read only explicitly granted repositories and cannot change settings.
New repositories receive no inherited viewer grant. Grant and role changes revoke
the affected sessions, so users sign in again. At least one administrator must
remain enabled. Account administration and trial renewal remain available after
trial expiry.

## Upgrade and backup

Back up the database and matching repository/encryption-key storage before the
upgrade. Keep existing installation Secrets, database volumes and repository
claims. Do not delete volumes or regenerate the encryption key to fix sign-in.
Beta.1 has no local accounts or saved trial; upgrading requires first-admin
bootstrap and an owner-issued installation key for the new trial-enabled image.
