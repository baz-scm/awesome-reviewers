---
title: Validate configuration formats
description: Ensure configuration values use the correct data format expected by target
  systems and avoid duplication by sourcing from authoritative locations when possible.
  Mismatched formats can cause runtime failures, while duplicated configurations create
  maintenance overhead and inconsistency risks.
repository: facebook/react-native
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 123178
---

Ensure configuration values use the correct data format expected by target systems and avoid duplication by sourcing from authoritative locations when possible. Mismatched formats can cause runtime failures, while duplicated configurations create maintenance overhead and inconsistency risks.

When configuring external tools or actions, verify the expected input format:
```yaml
# Wrong: JSON array format when comma-separated string expected
discord_ids: "[ \"${{ env.oncall1 }}\", \"${{ env.oncall2 }}\" ]"

# Correct: Comma-separated string format
discord_ids: "${{ env.oncall1 }}, ${{ env.oncall2 }}"
```

For deployment targets and version specifications, prefer reading from authoritative sources rather than hardcoding:
```yaml
# Consider reading from package.json or project config instead of:
IOS_DEPLOYMENT_TARGET: "13.4"
XROS_DEPLOYMENT_TARGET: "1.0" 
MAC_DEPLOYMENT_TARGET: "10.15"
```

Always validate configuration formats against documentation and test with actual usage to prevent integration issues.