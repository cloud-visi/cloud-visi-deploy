# AWS S3 state with GitHub and GitHub Actions

Cloud-Visi reads Terraform repositories, available workflow evidence and the S3
state file last read. It does not execute Terraform, provision AWS resources or
continuously monitor your AWS account. Existing Azure connections remain supported.

## Connect GitHub

In **Settings → GitHub**, select the owner and repositories and provide a
fine-grained token restricted to those repositories. Use Contents, Pull requests
and Actions **Read-only**. Add Deployments **Read-only** only to read deployment
metadata. Enter secrets in the application, never in Git or a public issue.

Runs and attempts are retained separately. Supported Terraform output can establish
plan observations, successful completion summaries or actual Terraform failures.
Setup, OIDC and download failures are not automatically failed Terraform applies.
A green workflow or GitHub Deployment is metadata, not proof of Terraform apply.

Beta.3 recognizes full 40-character SHA pins for `actions/download-artifact` and
canonical local composite wrappers used by direct/reusable workflows. The parser
rejects parent-directory wrappers and native shell steps masquerading as local
actions. Output-only plans can remain unattributed; resource counts stay unknown
when no resource summary exists. Artifact metadata does not authenticate downloaded
plan bytes. Missing, denied, expired, oversized or rate-limited logs leave coverage
unconfirmed; failed refreshes retain previous observations with their qualifications.
GitHub Actions does not yet provide full Azure Pipelines parity or DORA coverage.

## Connect an existing S3 state backend

1. Give the **server** an AWS identity using your deployment's existing AWS SDK
   credential mechanism. That calling identity must be permitted to assume only
   the selected state-reader role. A role ARN entered in the UI alone is not a
   server identity.
2. Configure that reader role's trust for the calling principal and the matching
   external ID. Scope its permissions to the selected state objects with
   `s3:GetObject`; scope any necessary `s3:ListBucket` permission to the backend
   prefix. SSE-KMS state also needs narrowly scoped `kms:Decrypt` and a matching
   key policy. The product needs no Terraform apply, EC2 write or state-lock writes.
3. In **Settings → AWS**, select the repositories and enter the role ARN and
   external ID. State credentials are separate from the GitHub credential.
4. Confirm the Terraform root's S3 bucket, object key and region. Complete partial
   backend configuration in the root's state-target settings. Select one workspace
   per root; named workspaces use their own object key. Do not substitute a dev
   state file to make staging appear healthy.

A successful state read is needed before first target binding. Region-routing and
AssumeRole failures do not create empty snapshots. Beta.3 distinguishes S3 region
routing failures from an STS rejection nested inside S3 credential retrieval.
Check bucket region/backend routing for the former, and calling identity, role
trust and external ID for the latter. A missing object remains missing evidence.
Unsafe target changes after binding are blocked to protect existing history.

## Upgrade and tested boundaries

Keep your database and matching repository/encryption-key volume through upgrades.
Beta.3 uses the same trial verification key as beta.2. New successful log reads
record parser version 13; already successful historical logs are not silently
reparsed. Any historical repair is an explicit, bounded operator action.

The AWS/GitHub campaign exercised independent dev/staging states, module instances,
plan/apply separation, partial failures, reruns, central cross-repository checkouts,
read denial/recovery and scoped viewer behavior. Some cases used controlled replays.
All 50 cases remain in Review, with no final independent campaign acceptance.
Native gates/forks were tested in an approved public provider-free fixture;
existing private GitHub plan/policy restrictions remain. Its fork actor was a
member, so first-time outsider approval behavior is not certified. A live invalid
account was refused; successful cross-account reads are not certified. State copies
are separate resource claims, not proof of exclusive physical-resource ownership.

Custom S3 endpoints and China/GovCloud live reads are not certified by this
campaign. GCS and notifications are out of scope. See [release verification](release-verification.md).
