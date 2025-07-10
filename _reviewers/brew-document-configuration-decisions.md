---
title: Document configuration decisions
description: When making configuration changes, especially those that deviate from
  standard practices or involve deprecation notices, always include clear explanatory
  comments. Temporary modifications to configuration settings should document both
  the reason and expected duration of the exception.
repository: Homebrew/brew
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 44168
---

When making configuration changes, especially those that deviate from standard practices or involve deprecation notices, always include clear explanatory comments. Temporary modifications to configuration settings should document both the reason and expected duration of the exception.

For example, instead of:
```yml
set +o pipefail
DELIMITER="END_LABELS_$(LC_ALL=C tr -dc '[:alnum:]' </dev/urandom | head -c20)"
set -o pipefail
```

Prefer:
```yml
# Temporarily disable pipefail because the random string generation command may fail harmlessly
set +o pipefail
DELIMITER="END_LABELS_$(LC_ALL=C tr -dc '[:alnum:]' </dev/urandom | head -c20)"
set -o pipefail
```

For deprecation notices, clearly specify alternatives:
```yml
# Deprecated: this image will be retired after April 2023
# Use homebrew/ubuntu22.04 or homebrew/ubuntu24.04 instead
echo "The homebrew/ubuntu18.04 image is deprecated and will soon be retired..." > .docker-deprecate
```

When possible, use standardized tools for configuration tasks rather than custom solutions (e.g., `uuidgen` for generating unique identifiers).