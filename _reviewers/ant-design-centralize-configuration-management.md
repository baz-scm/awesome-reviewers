---
title: Centralize configuration management
description: Avoid duplicate configuration processing and keep configuration data
  properly centralized. When configuration utilities or hooks already exist, use them
  instead of manually processing the same data. Keep translations in locale files
  rather than embedding them directly in data structures, and prefer design tokens
  over hardcoded values for styling...
repository: ant-design/ant-design
label: Configurations
language: TSX
comments_count: 3
repository_stars: 95882
---

Avoid duplicate configuration processing and keep configuration data properly centralized. When configuration utilities or hooks already exist, use them instead of manually processing the same data. Keep translations in locale files rather than embedding them directly in data structures, and prefer design tokens over hardcoded values for styling configurations.

Example of avoiding duplicate processing:
```typescript
// ❌ Don't manually process config when utilities exist
const { previewMask } = previewConfig && typeof previewConfig === 'object' ? previewConfig : {};

// ✅ Use existing configuration hooks
const [contextPreviewConfig, contextPreviewRootClassName, contextPreviewMaskClassName] = 
  usePreviewConfig(contextPreview);
```

Example of proper configuration separation:
```typescript
// ❌ Don't embed translations in data
const colors = [
  {
    name: 'red',
    english: 'Dust Red',
    chineseDescription: '斗志、奔放',
  }
];

// ✅ Use locale keys and keep translations centralized
const colors = [
  {
    name: 'red',
    english: 'Dust Red',
    descriptionKey: 'colors.red.description',
  }
];
// Then use: locale[color.descriptionKey]
```

This approach improves maintainability, reduces duplication, and ensures configuration changes are centralized and consistent across the application.