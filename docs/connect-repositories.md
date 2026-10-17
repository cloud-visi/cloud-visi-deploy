# Connect your repositories

## Which repository should I choose?

Choose a repository on GitHub or Azure DevOps that contains Terraform `.tf` files. A repository you already work with is a useful starting point. Choose only repositories you are allowed to read and want this installation to track.

- A repository containing complete Terraform projects can provide code history and, with access configured, pipeline and state information.
- A repository containing only reusable modules can provide changes to module code. It does not contain the state of the Terraform projects that use those modules.
- A repository without Terraform code is not useful for Terraform change history.

You do not need to create resources or run `terraform apply`. Cloud-Visi reads existing information. Missing pipelines or optional state access should not prevent you from connecting code.

## Azure DevOps

Have these details ready:

- Organization and project names. In `https://dev.azure.com/organization/project`, these are the two names after the hostname.
- A Personal Access Token with **Code: Read** and **Build: Read**, for the project and repositories you want to connect.

In the setup form, choose Azure DevOps, enter those details, and select **Find repositories**. Choose repositories in the selection panel and save the connection. A token can only discover repositories its account can access.

Reference: [Azure DevOps Personal Access Tokens](https://learn.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate).

## GitHub

Create a fine-grained token for the repository owner, restricted to the repositories you want to connect. Grant read access to **Contents**, **Pull requests**, **Actions**, and **Deployments**. GitHub includes metadata access automatically. Your organization may require approval before the token can read its repositories.

In the setup form, choose GitHub and follow the fields to select and save your repositories. This product token is separate from registry access. Public release images do not require a GitHub token to download.

Reference: [GitHub token permissions](https://docs.github.com/en/rest/authentication/permissions-required-for-fine-grained-personal-access-tokens).

## Terraform state is optional

You can connect code first and add state access later in Settings.

State reads need a Terraform project with backend configuration and access to the state file. Supported state stores are Azure Blob Storage for `azurerm` and AWS S3 for `s3`. A module-only folder has no independent Terraform state to read. Pipeline-provided backend details may not be visible in repository code.

For Azure, use a service principal with **Storage Blob Data Reader** on the state storage you want to read. Enter its tenant ID, client ID, and client secret in Settings. Do not grant subscription-wide write access.

For AWS, the server first needs an AWS identity. That identity must be allowed to assume the read-only role whose ARN and external ID you enter in Settings. That role needs access to the chosen S3 state object. An existing workload identity can supply the server identity; entering a role ARN alone does not do so. Ask your platform team to configure the deployment's identity if needed. You can continue without AWS state access.

## First sync and later changes

The first sync reads history from the configured lookback period, which defaults to 30 days. Its duration depends on the size of your repositories and access to the connected services.

Repository settings show sync progress and issues. They also let you manage repositories you no longer want to track. State checks can remain unavailable while code history is readable. See [available information](available-information.md) for how to interpret these differences.

For the AWS S3 and GitHub Actions path, see [AWS and GitHub setup](aws-github.md), including role scope, evidence formats and limits.
