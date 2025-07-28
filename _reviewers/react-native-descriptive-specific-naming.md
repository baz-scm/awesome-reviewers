---
title: descriptive specific naming
description: Use descriptive and specific names that clearly communicate purpose and
  context. Method names should indicate their platform target when applicable, test
  names should describe the expected behavior, and function names should follow consistent
  conventions.
repository: facebook/react-native
label: Naming Conventions
language: JavaScript
comments_count: 4
repository_stars: 123178
---

Use descriptive and specific names that clearly communicate purpose and context. Method names should indicate their platform target when applicable, test names should describe the expected behavior, and function names should follow consistent conventions.

**Platform-specific methods**: Include the platform in the method name to avoid confusion:
```javascript
// Instead of
isCatalogAsset(): boolean

// Use
isIOSCatalogAsset(): boolean
```

**Test naming**: Test names should be self-explanatory so engineers understand the purpose without reading implementation:
```javascript
// Instead of
it('Should view properly submit cancel text', async function () {

// Use  
it('Press Cancel Button - Validates cancel confirmation message displays', async function () {
```

**Function naming consistency**: Use camelCase for functions and underscore prefix for private methods:
```javascript
// Instead of
function _download_prebuild_release_tarball(

// Use
function _downloadPrebuildReleaseTarball(
```

Names should eliminate ambiguity about what code does, which platform it targets, or what behavior it tests. When reviewing code, ask: "Can I understand this element's purpose from its name alone?"