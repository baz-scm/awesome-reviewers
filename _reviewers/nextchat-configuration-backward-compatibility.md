---
title: Configuration backward compatibility
description: When modifying configuration schemas or adding new configuration options,
  always ensure backward compatibility with existing deployments. Long-running systems
  with many user deployments require smooth migration paths from old configurations
  to new ones.
repository: ChatGPTNextWeb/NextChat
label: Configurations
language: TypeScript
comments_count: 2
repository_stars: 85721
---

When modifying configuration schemas or adding new configuration options, always ensure backward compatibility with existing deployments. Long-running systems with many user deployments require smooth migration paths from old configurations to new ones.

Key practices:
1. **Validate both old and new formats**: Check for the presence of new format indicators before applying new logic
2. **Provide fallback handling**: When new configuration format is not detected, gracefully handle the old format
3. **Avoid breaking existing configs**: Don't assume all users will immediately update their configuration files

Example from model configuration handling:
```typescript
// Check for new format first
if (defaultModel.includes('@')) {
  // New format: model@provider
  if (defaultModel in modelTable) {
    modelTable[defaultModel].isDefault = true;
  }
} else {
  // Old format: just model name - find first matching model
  for (const key in modelTable) {
    if (key.split('@').shift() === defaultModel) {
      modelTable[key].isDefault = true;
      break;
    }
  }
}
```

This approach ensures that users with existing configurations can continue using the system without forced updates, while new users benefit from improved configuration options.