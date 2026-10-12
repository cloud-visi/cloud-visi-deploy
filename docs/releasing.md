# Maintainer release procedure

Partners install a released image. They do not build or publish product code.

The beta image publication was explicitly authorized for design partner validation.
The licence remains undecided. OCI chart publication stays on hold.

## Beta image publication

1. Build an OCI archive from a clean, approved private product commit, including
   Linux AMD64 and ARM64 images, SBOMs and minimal provenance. Set
   `BUILDX_GIT_INFO=false` to keep private source-control details out of provenance.
2. Record the image digest, archive checksum, source revision and actual build
   time in `releases/<version>.json`. Inspect runtime layers for source checkouts,
   environment files and private data before uploading.
3. Run `scripts/verify-image-archive.py` with the archive and its release record,
   the product tests and deployment checks. Record which runtime checks ran.
4. Upload only the verified runtime archive to a beta GitHub prerelease. Its
   checksum and image digest must match the approved record.
5. Run `Publish approved beta image` when image publication has been explicitly
   authorized. The initial publisher bootstrap runs only when its workflow file
   changes on `codex/beta-image-release`; documentation changes do not publish.
   Later runs are manual. The job has repository read and package write access,
   downloads the approved public archive and never checks out private source.
6. The publisher verifies the archive, keeps an existing version immutable,
   uploads the versioned image and `beta` alias, and checks their digests.
   It does not move `latest` or publish a chart.
7. Make the package public, verify downloads without registry credentials on
   both architectures, and update release notes with actual checks and limits.

The private product build helper's general publishing mode still requires licence
and evaluation-term files. This explicitly approved beta uses the verified archive
publisher. No product licence or evaluation terms were selected by this process.

## Chart publication remains on hold

Install the local chart files and select the beta image explicitly. Do not run
`helm push` until chart publication is authorized. Before publishing a chart,
select its reviewed version, pin the image digest, run a fresh local install,
and verify anonymous OCI chart downloads. Record its digest and tested versions.

The public repository contains deployment files, documentation and screenshots.
Its normal CI validates those files. It does not mirror or build product source.

References: [GHCR](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry), [Docker provenance](https://docs.docker.com/build/metadata/attestations/slsa-provenance/), [ORAS OCI archive copy](https://oras.land/docs/commands/oras_cp/).
