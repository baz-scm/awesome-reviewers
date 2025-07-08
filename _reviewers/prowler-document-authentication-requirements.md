---
title: Document authentication requirements
description: 'When creating or modifying APIs, always provide comprehensive documentation
  for authentication methods and prerequisites. For each authentication approach:'
repository: prowler-cloud/prowler
label: API
language: Markdown
comments_count: 4
repository_stars: 11834
---

When creating or modifying APIs, always provide comprehensive documentation for authentication methods and prerequisites. For each authentication approach:

1. Clearly state all supported authentication methods with explicit code examples
2. Document the exact permissions required for each method
3. Highlight any limitations or differences between authentication approaches
4. Specify all prerequisite APIs or services that need to be enabled
5. Include configuration requirements for billing and resource allocation

For example:

```markdown
### Authentication Methods

#### Service Principal Authentication
```console
prowler microsoft365 --sp-env-auth
```
- Requires: Directory.Read.All, Policy.Read.All permissions
- Provides access to all service functionality

#### Browser Authentication
```console
prowler microsoft365 --browser-auth --tenant-id "XXXXXXXX"
```
- Uses delegated permissions (assigned to user, not app)
- Limited to MS Graph API checks only
- Will not run all provider checks

### Prerequisites
- Identity and Access Management (IAM) API must be enabled:
  ```console
  gcloud services enable iam.googleapis.com --project <your-project-id>
  ```
- Quota project must be configured:
  ```console
  gcloud auth application-default set-quota-project <project-id>
  ```
```

Complete authentication documentation helps users successfully implement your API while avoiding unexpected permission issues or missing dependencies.