---
title: Structured changelog documentation
description: 'Maintain consistent and informative changelog documentation by following
  these practices:


  1. Structure changelogs with an "Unreleased" section at the top where all pending
  changes are documented before release'
repository: open-telemetry/opentelemetry-python
label: Documentation
language: Markdown
comments_count: 3
repository_stars: 2061
---

Maintain consistent and informative changelog documentation by following these practices:

1. Structure changelogs with an "Unreleased" section at the top where all pending changes are documented before release
2. Each PR that makes a relevant change should add an entry under the "Unreleased" section
3. When making a release, move items from "Unreleased" to a version-specific section
4. Clearly mark breaking changes (e.g., with "[BREAKING]" prefix)
5. Include explanations for technical changes, not just what was changed but why

Example:
```markdown
# Changelog

## Unreleased
- [BREAKING] Remove `opentelemetry.semconv.attributes.network_attributes.NETWORK_INTERFACE_NAME` due to deprecation in the specification
- Add `Final` decorator to constants to prevent accidental reassignment in strongly-typed code

## v1.0.0 (2023-04-01)
- Initial stable release
- Fix span context manager typing by using ParamSpec from typing_extensions
```

This approach ensures users and developers can easily track changes, understand their impact, and prepare for upgrades appropriately.