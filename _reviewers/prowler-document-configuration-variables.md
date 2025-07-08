---
title: Document configuration variables
description: Always provide complete documentation for configuration variables, including
  their exact format, purpose, and behavior. For environment variables and connection
  strings, specify the full expected format with examples and explain why specific
  formats are required.
repository: prowler-cloud/prowler
label: Configurations
language: Markdown
comments_count: 4
repository_stars: 11834
---

Always provide complete documentation for configuration variables, including their exact format, purpose, and behavior. For environment variables and connection strings, specify the full expected format with examples and explain why specific formats are required.

When documenting configuration options:

1. **Specify the complete format** - Use the exact format needed, especially for connection strings that may appear to have redundant parts
   ```python
   # Good: Full connection string format explained
   # export PROWLER_DB_CONNECTION=sqlite://
   # Format includes "://" to support future DB integrations like MongoDB or Redis
   ```

2. **Clarify when configuration changes take effect** - Document whether changes apply immediately, on restart, or only for new operations
   ```markdown
   ???+ note
       The Mutelist configuration takes effect on the next scans.
   ```

3. **Document automatic detection behavior** - When environment variables can be detected automatically, specify the order of precedence
   ```markdown
   If no token is explicitly provided, Prowler will automatically attempt to authenticate using environment variables in the following order of precedence:
   
   1. `GITHUB_PERSONAL_ACCESS_TOKEN`
   2. `OAUTH_APP_TOKEN`
   3. `GITHUB_APP_ID` and `GITHUB_APP_KEY`
   ```

4. **Include activation requirements** - If additional steps are needed to apply configuration, document them clearly
   ```markdown
   The necessary modules will not be installed automatically by Prowler. Nevertheless, if you want Prowler to install them for you, you can execute the provider with the flag `--init-modules`, which will run the script to install and import them.
   ```

Thorough configuration documentation prevents confusion, reduces support requests, and ensures users can correctly configure the system for their specific needs.