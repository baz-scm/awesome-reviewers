---
title: Consistent text formatting
description: Ensure text formatting follows established guidelines and maintains consistency
  within the same context. This applies to documentation strings, localization files,
  user interface text, and error messages.
repository: discourse/discourse
label: Documentation
language: Yaml
comments_count: 2
repository_stars: 44898
---

Ensure text formatting follows established guidelines and maintains consistency within the same context. This applies to documentation strings, localization files, user interface text, and error messages.

When established formatting guidelines exist, follow them consistently. For example, prefer sentence case over title case in user-facing strings:

```yaml
# Good - follows sentence case guidelines
associated_accounts_by_provider:
  title: "Associated accounts by login method"
  labels:
    provider: "Login provider"
    no_accounts: "No associated accounts"

# Avoid - inconsistent title case
associated_accounts_by_provider:
  title: "Associated Accounts by Login Method"
  labels:
    provider: "Login Provider"
```

Additionally, maintain internal consistency within the same file or related contexts. Ensure similar elements use the same formatting patterns:

```yaml
# Good - consistent formatting across similar entries
theme_source: "Theme '%{name}'"
plugin_source: "Plugin '%{name}'"

# Avoid - inconsistent punctuation
theme_source: "Theme '%{name}'"
plugin_source: "Plugin: '%{name}'"
```

This practice improves user experience, maintains professional appearance, and reduces cognitive load for both users and developers.