---
title: Document configuration consistently
description: 'Ensure all configuration options are clearly documented and follow consistent
  naming and syntax conventions. This includes:


  1. **Explicitly document prerequisites** - Clearly state all required tools, dependencies,
  and environment variables needed for configuration. For example, when jq is required
  for processing:'
repository: bridgecrewio/checkov
label: Configurations
language: Markdown
comments_count: 6
repository_stars: 7667
---

Ensure all configuration options are clearly documented and follow consistent naming and syntax conventions. This includes:

1. **Explicitly document prerequisites** - Clearly state all required tools, dependencies, and environment variables needed for configuration. For example, when jq is required for processing:
   ```bash
   terraform show -json tfplan.binary | jq > tfplan.json
   ```

2. **Use proper syntax for configuration files** - When defining multiple options with the same key in JSON configurations, use arrays:
   ```json
   "//": [
     "checkov:skip=CVE-2023-123: ignore this CVE for this file",
     "checkov:skip=express[BC_LIC_2]: ignore license violations"
   ]
   ```

3. **Follow consistent naming conventions** - For configuration flags and environment variables:
   - Use prefixes like DISABLE_* for turning off features that are enabled by default
   - Document environment variables in a structured format with clear descriptions
   - Maintain consistent enumeration values (e.g., severity levels: `INFO`, `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`)
   - Use proper capitalization for product names (e.g., "Terraform Cloud / Enterprise")

4. **Place configurations in appropriate locations** - Environment variables should be documented in Settings blocks, and related configuration options should be grouped together.