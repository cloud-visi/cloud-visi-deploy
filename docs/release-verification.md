# Release validation record

Maintainer checks completed on 12 October 2026 using isolated local data and no
real code-host or cloud credentials. The beta image is published; the OCI chart remains unpublished.

| Check | Result |
| --- | --- |
| Deployment checks and Helm lint | All 12 checks pass; lint passes |
| Product database tests | Full Go suite passes; the seven baseline failures are fixed |
| Actions integration coverage | Both tests pass in their required disposable database |
| Linux ARM64 | Local build and native Kubernetes startup pass |
| Linux AMD64 | Local build and Docker-emulated startup on an ARM Mac pass |
| Bundled scanner on AMD64 | Runs as the application user and detects issues in a local sample without downloading checks |
| Backup and restore | Database restored into a separate database with its original key; saved test credential remains readable |
| Upgrade compatibility | Previous main image replaced by the partner image; database, encrypted credential and repository markers remain |
| Uninstall and reinstall | Both storage claims and installation Secret retained; explicit claim reuse recovers data |
| Optional Compose | Fresh startup and restart retention pass; updated AMD64 image starts successfully |

Kubernetes checks used Kubernetes 1.36.1, Helm 4.2.2 and PostgreSQL 16.15.
The application ran as user 10001 and Kubernetes PostgreSQL as user 999.
The old application image used its existing health endpoint during the upgrade
check. The partner image uses its database readiness endpoint.

## Remaining publication gates

- Leave the product licence undecided until the owner chooses otherwise.
- Keep OCI chart publication on hold.
- After chart publication is authorized, verify anonymous chart download and a fresh installation from its published digest.

Native AMD64 hardware has not been tested. There is no previous published partner
release, so the upgrade check uses the previous main application image.
Four opt-in diagnostic and performance tests were skipped in the Go suite.

Product source stays in the private product repository. The public repository
contains deployment files, documentation and screenshots only.

## Beta image record

Version `0.1.0-beta.1` and alias `beta` were explicitly authorized for publication.
The image is built from merged private main with AMD64 and ARM64 runtime manifests,
SBOMs and minimal provenance. The release record contains the immutable digest,
archive checksum, source revision and actual build timestamp. Archive validation
rejects source checkout files, environment files and unexpected release identity.
The beta release notes record the post-publication download and runtime checks.
