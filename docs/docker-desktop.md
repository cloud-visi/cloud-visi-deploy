# Docker Desktop with Kubernetes

You can use the same Helm chart on your computer.

1. Start Docker Desktop in Linux container mode.
2. Open Docker Desktop's Kubernetes view and create or enable its local cluster. The controls vary by Docker Desktop version.
3. Wait for the cluster to be ready.
4. Run `kubectl config get-contexts` and identify its local context. It is usually named `docker-desktop`.
5. Follow [Install with Helm](kubernetes.md), using that local context. You can add `-f examples/values-docker-desktop.yaml` to the Helm command.

The setup uses local cluster storage. The authenticated beta requires an existing trusted HTTPS proxy for browser access; plain HTTP port forwarding alone is insufficient. A cloud subscription is not needed to install the application.

Do not reset the Docker Desktop Kubernetes cluster while you want to keep your installation data. A cluster reset can remove the application and its storage.

If you prefer not to enable Kubernetes, use the [optional Compose setup](compose.md).

Reference: [Docker Desktop Kubernetes documentation](https://docs.docker.com/desktop/use-desktop/kubernetes/).
