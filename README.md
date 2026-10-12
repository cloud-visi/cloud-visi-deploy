# Cloud-Visi deployment

Cloud-Visi is a self-hosted tool for understanding changes to Terraform code and the evidence available from pipelines and Terraform state.

This repository contains deployment files and partner guides. Product source is maintained separately.

**Release status:** the first preview is being prepared. The GHCR image and chart are not published yet. The installation commands below are for use after the first release is announced. No licence has been selected yet.

## Choose how to run it

| Your environment | Start here |
| --- | --- |
| A Kubernetes cluster | [Install with Helm](docs/kubernetes.md) |
| Docker Desktop with Kubernetes enabled | [Docker Desktop Kubernetes](docs/docker-desktop.md) |
| Docker Desktop without Kubernetes | [Optional Docker Compose setup](docs/compose.md) |

Kubernetes with Helm is the supported deployment path for this preview. Compose is an optional local setup.

## Before you connect a repository

Choose a GitHub or Azure DevOps repository that contains Terraform `.tf` files. Start with a repository you know and have permission to read. There is no need to create infrastructure, change a pipeline, or run Terraform to try the application.

A repository can contain several Terraform folders. Shared module repositories can provide code history, but modules by themselves do not provide the Terraform state of the projects that use them.

You will need a read-only token for your chosen code host. Terraform state access is optional. See [repository and credential setup](docs/connect-repositories.md).

## After installation

Open Cloud-Visi, choose your code host, and follow the setup form. Choose which repositories to connect. Cloud-Visi reads their existing history in the background, so the first sync can take some time.

Use it for your own work. There is no required evaluation task or prescribed outcome. If you want to share feedback, see [giving feedback](docs/feedback.md).

## More information

- [What information can be read](docs/available-information.md)
- [Configuration reference](docs/configuration.md)
- [Restart, upgrade, backup, and remove](docs/operations.md)
- [Troubleshooting](docs/troubleshooting.md)

## Access and data

The preview has no built-in login. Its Kubernetes service is reachable inside the cluster, so use a trusted namespace and network boundary. Keep access private. The default Helm instructions use port forwarding, and Compose binds only to localhost. Shared access requires your existing authentication gateway.

Repository copies, history, and saved credentials are stored in your installation. Code host and cloud connections use the credentials you provide. This deployment does not configure a hosted analytics service.

Public issues are visible to everyone. Do not attach tokens, Terraform state, private code, database backups, or unredacted logs.
