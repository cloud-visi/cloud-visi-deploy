# Release validation record

## Beta.4, 22 October 2026

Source: `948fde7beb2fd07edca39af17746b174499eab8c`. This release includes the customer
walkthrough fixes and the filter ordering regression caught during release checks.

| Check | Result |
| --- | --- |
| Fresh full Go suite with real-migration API tests | 2,137 pass events, 16 skip events, zero failures; 28 packages passed; events include subtests/packages |
| UI | 549 tests pass, zero skipped; TypeScript/Vite production build passes; lint has zero errors and 15 existing warnings |
| Deployment files | 21 tests and Helm lint pass |
| Source review | Backend scoping/security, adversarial review and coverage/scope audit have no remaining actionable findings; adversarial fixtures were summary-only |
| Filter ordering regression | Mixed-case person names reproduced the defect; the fixed order and repository-wide collation guard pass |
| Multi-architecture archive | AMD64/ARM64 manifests, UID 10001, SBOMs, provenance and no source checkout verified |
| Local ARM64 runtime | Config matches the exact archive; readiness, administrator bootstrap/login, version, configured trial verifier and bundled scanner pass |

Native GitHub AMD64 and ARM64 readiness, non-root user, administrator login, build identity, configured trial verifier and bundled scanner checks pass.

Both architectures are publicly available. Anonymous OCI registry downloads of both manifests and all runtime config/layer bytes passed SHA-256 checks (12 unique blobs, 136,209,626 bytes). The version and beta alias match the approved digest. Beta.1, beta.2 and beta.3 are unchanged; latest is absent and no OCI chart was published.

[Publication and native checks](https://github.com/cloud-visi/cloud-visi-deploy/actions/runs/39796825802) and
[deployment checks](https://github.com/cloud-visi/cloud-visi-deploy/actions/runs/39796581613) retain the job evidence. Local checks use disposable data, publish no
host ports and use no provider credentials. Existing local applications and data
are preserved; the application on port 8080 is unchanged.

The trial owner verification key is unchanged from beta.3. No schema migration
or new runtime service is added; keep database, encryption key and trial files.

The customer walkthrough used fictional examples with explicit labels. Separate
live administrator setup, GitHub discovery, first sync and refusal controls were
verified. Full live private Actions/state onboarding is not certified by that
walkthrough: refreshed GitHub fixture access and Azure state credentials are
still needed. The earlier AWS campaign retains 50 cases in Review and none
Closed, with independent acceptance pending. GitHub Actions evidence remains
partial; DORA retains its Azure Pipeline limit. No new operating envelope,
GCS support, notifications or OCI chart publication is claimed.

See the [release record](../releases/0.1.0-beta.4.json),
[changelog](../CHANGELOG.md) and [AWS evidence limits](aws-github.md).

## Beta.3, 17 October 2026

Source: `22344f62c0ea5bcddd89c15b933eb32575d3c162`, merged AWS fixes.
The tree exactly matches the independently reviewed source tested before PR merge.

| Check | Result |
| --- | --- |
| Full Go suite with real-migration API tests | 2,117 pass events, 16 skips, zero failures, 28 packages; events include subtests/packages |
| AWS fixture pack | Nine Python tests, nine actionlint workflow checks and Terraform formatting pass |
| Deployment checks | 21 tests and Helm lint pass |
| UI build | TypeScript/Vite production build passes during the image build |
| Multi-architecture archive | AMD64/ARM64 manifests, non-root UID 10001, SBOMs, provenance and no source checkout verified |
| Local ARM64 runtime | Exact archive runtime configuration digest; readiness, administrator bootstrap/login, build identity, trial verifier and bundled scanner pass |
| Published native AMD64 and ARM64 | Readiness, UID 10001, first administrator/login, build identity, trial verifier and bundled scanner pass |
| Anonymous image pulls | AMD64 and ARM64 downloads pass; beta.3 and beta match the approved digest |
| Previous tags | Beta.1/beta.2 unchanged; latest remains absent; OCI chart unpublished |

[Publication and native checks](https://github.com/cloud-visi/cloud-visi-deploy/actions/runs/39044313680),
[deployment checks](https://github.com/cloud-visi/cloud-visi-deploy/actions/runs/39044281598),
and [the release record](../releases/0.1.0-beta.3.json) retain the completed evidence.

The existing owner verification key is unchanged from beta.2. Historical log
repair remains explicit; new successful reads record parser version 13. The AWS
campaign has 50 cases in Review, none Closed; it is not independently accepted.
See [AWS coverage and qualifications](aws-github.md) and [the changelog](../CHANGELOG.md).
The two-hour partner soak was not repeated; no larger operating envelope is claimed.
Local release smoke tests use disposable data, no host ports and no provider
credentials. They do not populate the user's newly reset application.

## Beta.2, 17 October 2026

Fresh checks use clean private main `8a7a663eb3dbc57bfd2df45675fc8237b94797e6`
and disposable local data. No real code-host or state credentials are used.

| Check | Result |
| --- | --- |
| Go suite | 2,012 test/subtest pass events, 28 packages |
| Explicit auth/upgrade/scoping harness | 46 pass events, zero skips; overlaps the full suite |
| UI | 528 tests; lint and TypeScript/Vite production build pass |
| Go vet | Pass |
| Deployment | 21 tests and Helm lint pass with the required public origin |
| OCI archive | AMD64/ARM64 manifests, UID 10001, SBOMs, provenance and runtime layer checks pass |
| Local ARM64 runtime | First administrator, login, version identity, signed owner trial activation, product access and restart retention pass |
| GHCR publication | Version and beta alias match the approved archive digest |
| Native AMD64 and ARM64 | Readiness, UID 10001, administrator bootstrap/login, version identity, configured trial verification and bundled scanner pass |
| Anonymous GHCR downloads | Both architectures pass using an empty Docker credential configuration |
| Existing tags | Beta.1 unchanged; latest remains absent; OCI chart unpublished |

Diagnostic/performance tests remain opt-in. The passing two-hour partner soak
was completed on 15 October; it was not repeated for this image release.
The 25,000-resource comparison still falls outside the verified latency envelope.
See [the changelog](../CHANGELOG.md) for upgrade requirements and limits.
[Publication and native checks](https://github.com/cloud-visi/cloud-visi-deploy/actions/runs/39019872885) use the exact approved digest
and disposable data. [The release record](../releases/0.1.0-beta.2.json) records
the digest, checksum, build identity and anonymous download checks.
The existing application on port 8080 and its data are not changed by release checks.

## Beta.1 historical checks

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

The published beta also passes startup and scanner checks on native AMD64 and
ARM64 GitHub runners. There is no previous published partner release, so the
upgrade check uses the previous main application image.
Four opt-in diagnostic and performance tests were skipped in the Go suite.

Product source stays in the private product repository. The public repository
contains deployment files, documentation and screenshots only.

## Beta image record

Version `0.1.0-beta.1` and the then-current alias `beta` were explicitly authorized for publication.
The image is built from merged private main with AMD64 and ARM64 runtime manifests,
SBOMs and minimal provenance. The release record contains the immutable digest,
archive checksum, source revision and actual build timestamp. Archive validation
rejects source checkout files, environment files and unexpected release identity.
The beta release notes record the post-publication download and runtime checks.

Native post-publication checks passed on both `ubuntu-24.04` and
`ubuntu-24.04-arm`: architecture, UID 10001, database readiness, beta version,
source revision, build timestamp and bundled scanner. These use the exact
published digest and disposable local databases. Anonymous GHCR downloads passed for both AMD64 and ARM64 using an empty Docker
credential configuration. At beta.1 verification time its versioned tag and `beta` alias resolved to the
recorded image digest; `beta` is a moving alias for the newest approved beta. The compiled OCI archive is also available without
authentication as a GitHub release asset.
