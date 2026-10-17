# Install with Helm

The beta image is public and can be downloaded without registry credentials. The OCI chart remains on hold, so install the chart files from this repository and select the beta image explicitly.

## What you need

- Access to a Kubernetes cluster and permission to create resources in your chosen namespace.
- `kubectl`, Helm, Python 3, and Git on your computer.
- A default storage class, or the name of a storage class you can use.
- Network access from the cluster to GHCR, the PostgreSQL image registry, and the code host you will connect.

The chart uses one application pod and, by default, one PostgreSQL pod. It requests 5 GiB for repository storage and 10 GiB for database storage. These sizes and resource requests are adjustable. They are starting values for evaluation, not measured capacity guarantees.

## 1. Download the deployment files

```bash
git clone https://github.com/cloud-visi/cloud-visi-deploy.git
cd cloud-visi-deploy
```

Use the repository tag that matches the release instructions when one is available.

## 2. Choose the cluster

```bash
kubectl config get-contexts
```

Set `CONTEXT` to the context you want to use. Every command below names that context explicitly.

```bash
CONTEXT=your-context-name
kubectl --context "$CONTEXT" create namespace cloud-visi
```

If the namespace already exists, keep it and continue.

## 3. Create the installation credentials

```bash
python3 scripts/create-kubernetes-secret.py --context "$CONTEXT"
```

This creates a database password and the key used to encrypt saved application credentials. It does not display their values. If the Secret already exists, the script keeps it.

This is separate from your GitHub or Azure DevOps token, which you enter in the application later. Keep the installation Secret for upgrades and recovery.

## 4. Install the chart

Select the image version listed on the release page.

```bash
IMAGE_VERSION=0.1.0-beta.2
PUBLIC_URL=https://your-cloud-visi-hostname.example
helm upgrade --install cloud-visi ./charts/cloud-visi \
  --set image.tag="$IMAGE_VERSION" --set config.authPublicURL="$PUBLIC_URL" \
  --kube-context "$CONTEXT" --namespace cloud-visi \
  --wait --timeout 10m
```

The first start creates the database tables before accepting requests. If installation does not finish, use [troubleshooting](troubleshooting.md).

For a specific storage class, add:

```bash
--set persistence.storageClass=your-storage-class --set postgresql.storage.storageClass=your-storage-class
```

## 5. Open the application

Route the private service through your existing trusted TLS proxy or ingress,
using the exact HTTPS origin passed as `config.authPublicURL`. Preserve public
Host and Origin headers and restrict direct backend access. The chart does not
provision TLS or an authentication gateway.

Complete [operator administrator bootstrap](access-control.md), sign in at the
configured HTTPS origin, [activate the trial](trial.md), then
[connect a repository](connect-repositories.md). Plain HTTP port forwarding alone
does not provide the secure browser session required by this release.

## Use your existing PostgreSQL database

Use PostgreSQL 16 with UTF8 encoding and ICU Unicode collation support. Create a dedicated database and a user allowed to create the application tables and run migrations. The application also needs normal read and write access to its own data.

Before creating the Secret, run the script with `--external-database`. It asks for the database connection URL without displaying it:

```bash
python3 scripts/create-kubernetes-secret.py --context "$CONTEXT" --external-database
```

Use a trusted TLS connection for a remote database. Do not put the URL in a public values file or shell command. If a Secret already exists for a different database, choose a different Secret name and set `secrets.existingSecret` to match it.

Install with the same Helm command and add:

```bash
-f examples/values-external-postgres.yaml
```

This disables the bundled PostgreSQL pod. You manage backup and recovery for the external database.
