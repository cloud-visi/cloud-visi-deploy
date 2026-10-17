# Changelog

## 0.1.0-beta.3 - 2026-10-17

Source: `22344f62c0ea5bcddd89c15b933eb32575d3c162` (merged AWS fixes).

### AWS and GitHub Actions

- Validate the existing AWS S3 state-reader and GitHub Actions path with a
  50-case campaign, six private fixture repositories and scoped replay tests.
- Recognize full-SHA artifact action pins and output-only plans behind canonical
  local composite wrappers, including reusable workflow forms.
- Report typed S3 region-routing failures and STS credential failures nested
  inside S3 reads with the correct explanation. Failed reads retain state history.
- Explain current GitHub delivery evidence and log coverage accurately; workflow
  success never implies Terraform apply or current cloud state.
- Reject parent-directory action paths and native shell steps that resemble local
  composites. Legitimate indented action inputs named shell remain supported.
- Add [AWS/GitHub setup and evidence limits](docs/aws-github.md).

### Upgrade and verification

- Parser version 13 applies to new successful reads; historical repair stays
  explicit and bounded. Preserve the database and matching encryption-key storage.
- Administrator sign-in and installation-bound trials continue from beta.2 with
  the same owner verification key. No schema migration or new runtime service.
- Final tested source: 2,117 Go pass events, 16 skips, zero failures across 28
  packages, with real-migration API coverage. Events include subtests/packages.
  Nine fixture tests, nine actionlint checks, Terraform formatting and server
  build pass. The merged main tree matches that reviewed/tested source exactly.
- The campaign's 50 cases are in Review, none Closed; overall independent
  acceptance is pending. Public gate/fork variants do not certify private
  features or first-time outsider behavior. Invalid-account refusal does not
  certify a successful cross-account read. Some controls are controlled replays.
- GitHub Actions coverage remains partial; DORA retains its Azure Pipeline limit.
  State is an observation, not continuous cloud health or apply causality.
- GCS, notifications, automatic remediation and OCI chart publication remain
  excluded. No new scale or vulnerability-free dependency claim is made.
- Image/archive checks and publication status are recorded in
  [release verification](docs/release-verification.md) and the versioned record.

## 0.1.0-beta.2 - 2026-10-17

Source: `8a7a663eb3dbc57bfd2df45675fc8237b94797e6`.

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

- AMD64 and ARM64 native readiness, sign-in, version and bundled scanner checks
  passed against the published digest. Both architectures download anonymously.
  The beta.1 image is unchanged; no `latest` tag or OCI chart was published.
  See [image verification](docs/release-verification.md) and the
  [release record](releases/0.1.0-beta.2.json).

- Fresh release verification: 2,012 Go test/subtest pass events across 28 packages,
  46 explicit auth/upgrade/scoping harness pass events and 528 UI tests. UI lint,
  TypeScript/Vite build, Go vet, 21 deployment checks and Helm lint passed.
  Harness counts overlap the full suite; diagnostic/performance tests are opt-in.
- The verified synthetic partner profile is 20 repositories, 5,000 resources,
  50,000 changes and five readers, including a passing uninterrupted two-hour soak.
- The 25,000-resource comparison still misses latency targets and is outside that
  verified envelope. Synthetic results are not a customer workload guarantee.
- GitHub Actions coverage remains partial; DORA retains its Azure Pipeline limit.
- Available state is an observation, not continuous cloud health or apply causality.
- GCS, notifications, automatic remediation and OCI chart publication are excluded.
- The locked UI build dependency `source-map-js` 1.2.1 has a
  [known source-map denial-of-service advisory](https://github.com/advisories/GHSA-68fv-2mgg-jv7q).
  It processes the trusted release source during build; the runtime image ships
  the compiled static UI and Go server, without Node.js or that build package.
  This release is not a claim of a vulnerability-free dependency inventory.

## 0.1.0-beta.1 - 2026-10-12

Initial public beta runtime for Linux AMD64 and ARM64, with non-root execution,
bundled Terraform security checks, readiness probes, SBOMs and provenance.
This older image has no application login or trial enforcement.
