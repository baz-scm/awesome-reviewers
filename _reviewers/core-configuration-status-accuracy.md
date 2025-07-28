---
title: configuration status accuracy
description: Ensure that configuration file status values accurately reflect the actual
  implementation state. Use 'done' only when features are fully implemented, 'todo'
  for planned but unimplemented features, and 'exempt' for features that don't apply
  to the integration. Always provide clear, descriptive comments explaining why items
  are marked as exempt.
repository: home-assistant/core
label: Configurations
language: Yaml
comments_count: 3
repository_stars: 80450
---

Ensure that configuration file status values accurately reflect the actual implementation state. Use 'done' only when features are fully implemented, 'todo' for planned but unimplemented features, and 'exempt' for features that don't apply to the integration. Always provide clear, descriptive comments explaining why items are marked as exempt.

Example from quality scale configuration:
```yaml
rules:
  inject-websession: todo  # Not 'done' if not actually implemented
  entity-event-setup:
    status: exempt
    comment: no explicit subscriptions to events
  dynamic-devices:
    status: exempt
    comment: |
      No dynamic devices possible.
```

This prevents misleading configuration states and helps maintainers understand the true implementation status and reasoning behind exemptions.