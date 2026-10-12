# Information Cloud-Visi can read

Cloud-Visi combines information that is available to your installation. A connection does not guarantee that every kind of evidence exists or is readable.

| Information | Source | What it means |
| --- | --- | --- |
| Terraform code changes | Repository commits and `.tf` files | What changed in code |
| Pull requests and reviews | GitHub or Azure DevOps | Review information available from the code host |
| Pipeline activity | Azure Pipelines or GitHub Actions | Runs and the execution details the product can read |
| Terraform plan or apply details | Supported pipeline outputs | Available details depend on the workflow and output format |
| Terraform state | Azure Blob Storage or AWS S3 | Resources and values in the state file last read |
| Findings | Analysis of readable Terraform code and state | Additional context; Cloud-Visi is a change intelligence product |

A successful pipeline run alone does not prove that Terraform applied a change. A plan describes proposed changes. A failed apply can have made partial changes. Terraform state is stored evidence and is not a direct live inventory of a cloud account.

GitHub Actions evidence currently has limits. Cloud-Visi can read runs and some Terraform results, but it does not support every workflow format or provide full parity with Azure Pipelines. Mixed-provider improvements are a separate development stream and are not promised by this preview.

Branch policy information does not determine whether repository sync is healthy. Cloud-Visi is not a branch protection compliance tool.

If you encounter missing information, you can share what you were trying to understand. You do not need to change your normal workflow just to complete an evaluation.
