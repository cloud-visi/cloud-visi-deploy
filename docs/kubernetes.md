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
IMAGE_VERSION=0.1.0-beta.1
helm upgrade --install cloud-visi ./charts/cloud-visi \
  --set image.tag="$IMAGE_VERSION" \
  --kube-context "$CONTEXT" --namespace cloud-visi \
  --wait --timeout 10m
```

The first start creates the database tables before accepting requests. If installation does not finish, use [troubleshooting](troubleshooting.md).

For a specific storage class, add:

```bash
--set persistence.storageClass=your-storage-class --set postgresql.storage.storageClass=your-storage-class
```

## 5. Open the application

```bash
kubectl --context "$CONTEXT" -n cloud-visi port-forward service/cloud-visi 8080:8080
```

Keep that terminal open and visit http://127.0.0.1:8080. If that port is already in use, forward `8081:8080` and visit port 8081 instead.

Next: [connect a repository](connect-repositories.md).

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
