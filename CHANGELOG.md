# Changelog

## 0.1.0-beta.2 - release candidate

Source: `8a7a663eb3dbc57bfd2df45675fc8237b94797e6`.
This entry describes the candidate. Image publication and architecture checks must
complete before it is marked released.

### Added

- Local administrator sign-in, revocable sessions, repository-scoped viewer
  grants, account administration, CSRF protection and authenticated snapshots.
- Installation-bound trials, with signed offline keys valid for up to 30 days.
  Expiry pauses access and sync while preserving data and renewal access.
- Durable repository identity across providers, server scopes and reconnection;
  independent commit membership for mirrored repositories.
- Separate Terraform plan, apply and state observations, retained run attempts,
  explicit cross-repository attribution and independent source/cloud filters.
- Backend identity and configuration resolution with one selected workspace per
  root and protection against unsafe target changes.
- Dependencies through locals, variables and scoped modules; retained graph
  generations, explicit historical reparse and scoped Azure/S3 cross-state paths.

### Changed

- Integrates the Graphite & Butter interface colours with all approved features.
- Bounds scoped queries and evidence enrichment, and limits browser request
  concurrency so authentication and trial checks remain responsive.
- Missing evidence remains unconfirmed. A successful workflow or a resource in a
  later state snapshot does not prove that a particular Terraform apply succeeded.

### Upgrade requirements

- Back up the database and matching repository/encryption-key storage. Keep both
  through the upgrade; do not remove volumes or replace the encryption key.
- Configure `AUTH_PUBLIC_URL` to the exact HTTPS origin behind your existing
  trusted TLS proxy. New and upgraded installations require operator bootstrap
  of the first administrator. See [access setup](docs/access-control.md).
- Sign in before activating the installation-bound trial. Existing beta.1 installs
  have no saved trial and need an owner-issued key for this release.
- Application migrations are additive. Historical reparse/repair commands remain
  explicit operator actions; no historical campaign is run by this release.

### Verification and limits

- Source verification on 15 October: 2,053 Go tests/subtests, 48 explicit harness
  checks and 528 UI tests passed. Release-specific checks are recorded separately.
- The verified synthetic partner profile is 20 repositories, 5,000 resources,
  50,000 changes and five readers, including a passing uninterrupted two-hour soak.
- The 25,000-resource comparison still misses latency targets and is outside that
  verified envelope. Synthetic results are not a customer workload guarantee.
- GitHub Actions coverage remains partial; DORA retains its Azure Pipeline limit.
- Available state is an observation, not continuous cloud health or apply causality.
- GCS, notifications, automatic remediation and OCI chart publication are excluded.

## 0.1.0-beta.1 - 2026-10-12

Initial public beta runtime for Linux AMD64 and ARM64, with non-root execution,
bundled Terraform security checks, readiness probes, SBOMs and provenance.
This older image has no application login or trial enforcement.
