---
title: Actions configuration best practices
description: 'When working with GitHub Actions workflows, follow these configuration
  best practices:


  1. **Boolean inputs comparison**: GitHub Actions boolean inputs are actually strings.
  Always use string comparison with quotes:'
repository: n8n-io/n8n
label: Configurations
language: Yaml
comments_count: 4
repository_stars: 122978
---

When working with GitHub Actions workflows, follow these configuration best practices:

1. **Boolean inputs comparison**: GitHub Actions boolean inputs are actually strings. Always use string comparison with quotes:

```yaml
# ❌ Incorrect - may never evaluate as expected
if: ${{ inputs.enable-docker-cache == true }}

# ✅ Correct - properly compares string values
if: ${{ inputs.enable-docker-cache == 'true' }}
```

2. **Version pinning**: Always pin external GitHub Actions to specific commit SHAs rather than using major version tags:

```yaml
# ❌ Insecure - may pull unexpected updates
uses: actions/checkout@v4

# ✅ Secure - pins to specific commit
uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
```

3. **Input naming consistency**: Maintain consistent input naming across workflow triggers. Ensure variables referenced in workflows match the input names defined in `workflow_call` and `workflow_dispatch` events to avoid undefined values.

4. **Dynamic identifiers**: Include both run ID and attempt ID in dynamically generated values like branch names to ensure uniqueness across workflow reruns:

```yaml
# ✅ Better uniqueness for branches created in workflows
branch: 'chore/openapi-sync-${{ github.run_id }}-${{ github.run_attempt }}'
```

These practices improve security, reliability, and maintainability of workflow configurations.