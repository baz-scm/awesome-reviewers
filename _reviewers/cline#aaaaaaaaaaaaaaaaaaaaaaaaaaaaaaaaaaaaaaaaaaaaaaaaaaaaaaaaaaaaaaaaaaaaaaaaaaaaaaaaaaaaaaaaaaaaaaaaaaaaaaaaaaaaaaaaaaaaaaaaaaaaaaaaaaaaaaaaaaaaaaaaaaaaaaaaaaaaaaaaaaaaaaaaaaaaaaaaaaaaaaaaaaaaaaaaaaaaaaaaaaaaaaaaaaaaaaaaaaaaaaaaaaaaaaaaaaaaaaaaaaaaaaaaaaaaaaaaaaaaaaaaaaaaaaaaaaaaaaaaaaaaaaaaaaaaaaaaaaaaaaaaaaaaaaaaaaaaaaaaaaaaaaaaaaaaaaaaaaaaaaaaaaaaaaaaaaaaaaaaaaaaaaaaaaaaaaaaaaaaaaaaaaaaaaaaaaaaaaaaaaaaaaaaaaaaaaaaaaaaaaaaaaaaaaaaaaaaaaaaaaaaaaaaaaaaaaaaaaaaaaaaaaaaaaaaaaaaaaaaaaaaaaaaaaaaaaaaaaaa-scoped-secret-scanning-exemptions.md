---
title: Scoped secret-scanning exemptions
description: When adding allowlist/exemption entries to secret-scanning configurations
  (e.g., .gitleaks.toml), scope them as narrowly as possible so they only exclude
  the specific known-safe values (such as synthetic test IDs or placeholder credentials)
  rather than broadly disabling detection for a whole pattern or file path. Use precise
  match conditions (e.g.,...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Security
language: Toml
comments_count: 1
repository_stars: 70964
---

When adding allowlist/exemption entries to secret-scanning configurations (e.g., .gitleaks.toml), scope them as narrowly as possible so they only exclude the specific known-safe values (such as synthetic test IDs or placeholder credentials) rather than broadly disabling detection for a whole pattern or file path. Use precise match conditions (e.g., condition = AND with regexTarget = match) to combine multiple criteria, ensuring the exemption applies only to the exact strings intended. After adding any exemption, verify that unrelated or similarly-formatted secrets at the same location are still correctly detected by the scanner, to confirm the allowlist hasn't inadvertently widened the blind spot for real credentials. Document the reason for each exemption inline so future maintainers understand why it's safe.</description>
</invoke>
