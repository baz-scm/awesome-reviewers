---
title: Configuration merging precedence
description: When merging configuration objects, always preserve existing values and
  follow clear precedence rules to avoid unintentionally overriding settings. Use
  spread operators carefully and ensure the merge logic is implemented at the appropriate
  layer (preferably in action/store layer rather than component level).
repository: lobehub/lobe-chat
label: Configurations
language: TSX
comments_count: 3
repository_stars: 65138
---

When merging configuration objects, always preserve existing values and follow clear precedence rules to avoid unintentionally overriding settings. Use spread operators carefully and ensure the merge logic is implemented at the appropriate layer (preferably in action/store layer rather than component level).

**Key principles:**
1. **Preserve existing values**: When conditionally adding properties, avoid using empty objects `{}` that can override existing configurations
2. **Clear precedence order**: Establish and document which configuration source takes priority (e.g., user settings > default settings > provider settings)
3. **Merge at the right layer**: Implement merging logic in store actions rather than components for consistency across the application

**Examples:**

❌ **Problematic merging** - overwrites existing footerAction:
{% raw %}
```tsx
appearance={{
  ...appearance,
  elements: {
    ...appearance.elements,
    footerAction: !enableClerkSignUp ? { display: 'none' } : {}, // Empty object overwrites existing
  }
}}
```
{% endraw %}

✅ **Proper conditional merging**:
{% raw %}
```tsx
appearance={{
  ...appearance,
  elements: {
    ...appearance.elements,
    ...((!enableClerkSignUp) && { footerAction: { display: 'none' } }),
  }
}}
```
{% endraw %}

❌ **Component-level merging**:
```tsx
onChange={(value) => {
  updatePluginSettings(id, { [item.name]: value }); // Overwrites other settings
}}
```

✅ **Store-level merging**:
```tsx
// In store action
updatePluginSettings: (id, updates) => {
  set((state) => ({
    pluginSettings: {
      ...state.pluginSettings,
      [id]: { ...state.pluginSettings[id], ...updates }
    }
  }));
}
```

This approach ensures configuration integrity and prevents accidental loss of user preferences or system settings.