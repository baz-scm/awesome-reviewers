---
title: maintain cross-platform API consistency
description: When designing APIs that work across multiple platforms, ensure consistent
  return types and behavior to avoid breaking changes and maintain a unified developer
  experience. Use Platform.select() to handle platform-specific implementations rather
  than hardcoded conditional logic.
repository: facebook/react-native
label: API
language: JavaScript
comments_count: 2
repository_stars: 123178
---

When designing APIs that work across multiple platforms, ensure consistent return types and behavior to avoid breaking changes and maintain a unified developer experience. Use Platform.select() to handle platform-specific implementations rather than hardcoded conditional logic.

For APIs that need different implementations per platform, structure the code to provide consistent types while allowing platform-specific behavior:

```javascript
return Platform.select({
  android: this.isLoadedFromFileSystem()
    ? this.drawableFolderInBundle()
    : this.resourceIdentifierWithoutScale(),
  ios: this.isCatalogAsset()
    ? this.assetFromCatalog()
    : this.scaledAssetURLNearBundle(),
  default: this.scaledAssetURLNearBundle()
});
```

When a platform cannot provide meaningful data, return a consistent placeholder value rather than undefined or void types. For example, if web platforms cannot provide an OS version, return a stable string like "1000.0.0" to maintain type consistency across all platforms. This prevents breaking changes for consumers who expect consistent API contracts regardless of the underlying platform.