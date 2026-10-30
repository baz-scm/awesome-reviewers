---
title: Scope secret-scanning allowlists narrowly
description: When adding exceptions to secret-scanning tools (e.g., gitleaks allowlists)
  for known-safe values such as synthetic test model IDs, scope the exemption as tightly
  as possible—combine conditions (e.g., `condition = AND`) with precise match targeting
  (e.g., `regexTarget = match`) and specific file paths/regex patterns—rather than
  broadly disabling a rule or...
repository: 'cline/cline#

  zzprobe3b82974b: x'
label: Security
language: Toml
comments_count: 1
repository_stars: 71067
---

When adding exceptions to secret-scanning tools (e.g., gitleaks allowlists) for known-safe values such as synthetic test model IDs, scope the exemption as tightly as possible—combine conditions (e.g., `condition = AND`) with precise match targeting (e.g., `regexTarget = match`) and specific file paths/regex patterns—rather than broadly disabling a rule or path. After adding the exemption, verify with a test: confirm the intended synthetic/dummy values are ignored while any unrelated real credential placed in the same file or path is still flagged. This prevents allowlist entries from inadvertently masking genuine leaked secrets.

Example:
```toml
[[allowlists]]
description = "Synthetic model IDs are not real secrets"
paths = ['''path/to/test_models\.go''']
regexes = ['''sk-synthetic-[a-f0-9]{32}''']
regexTarget = "match"
condition = "AND"
```
</description>
