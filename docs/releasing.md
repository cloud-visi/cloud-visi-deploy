# Maintainer release procedure

This guide is for maintainers. Partners do not need to build images or publish charts.

The first release is blocked until the repository licence and image evaluation terms are approved. Repository creation is complete, but no package is published yet.

The completed local checks and remaining publication gates are recorded in
[Release validation](release-verification.md).

## Product build

Build the image from the approved private product commit using its `scripts/build-partner-image.sh`. Keep the source checkout private. Use the image version, source revision, and build time in the release record.

The build script defaults to a local build. Its publishing mode checks for approved licence files, produces AMD64 and ARM64 images, and includes dependency inventory and build provenance. Authenticate the publishing process using a dedicated publisher identity. Never reuse a product read-only connection token.

## Chart and release record

1. Run the product test suite with a disposable PostgreSQL database, the deployment checks, a fresh Helm install, and persistence checks.
2. Set the chart's `version` and `appVersion` to the release versions. Set `image.digest` to the published multi-platform image digest. Do not reuse an existing release tag.
3. Record the image digest, chart digest, source revision, tested versions, architectures, limitations, and any upgrade requirements in the release notes. Describe only checks that actually ran.
4. Package the chart with `helm package charts/cloud-visi`.
5. After licence approval and explicit publication authorization, authenticate to GHCR and push the chart with `helm push cloud-visi-<chart-version>.tgz oci://ghcr.io/cloud-visi/charts`.
6. Set both packages to public. GHCR packages start private unless visibility is explicitly changed.
7. Check image pulls and `helm show chart` from a clean registry configuration with no credentials. Follow the published install instructions from a fresh local cluster.
8. Publish matching documentation and release notes only after these checks pass.

No publishing workflow runs automatically from a documentation change. This repository does not fetch, mirror, or publish product source. Normal CI validates only deployment files.

References: [GHCR](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry), [Helm OCI charts](https://helm.sh/docs/v3/topics/registries/), [Docker multi-platform builds](https://docs.docker.com/build/building/multi-platform/).
