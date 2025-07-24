---
title: Simplify code readability
description: Prioritize code readability by using clearer control structures, extracting
  complex expressions into descriptive variables, and choosing simpler syntax when
  available. This improves maintainability and makes code easier to understand for
  other developers.
repository: argoproj/argo-cd
label: Code Style
language: TSX
comments_count: 4
repository_stars: 20149
---

Prioritize code readability by using clearer control structures, extracting complex expressions into descriptive variables, and choosing simpler syntax when available. This improves maintainability and makes code easier to understand for other developers.

Key practices:
- Use switch statements instead of multiple if-else chains for better readability
- Extract complex expressions into temporary variables with descriptive names
- Use fragment shorthand `<></>` instead of `<React.Fragment>` when keys aren't needed
- Simplify conditional logic by consolidating related operations

Example of improved readability:
```javascript
// Instead of multiple if-else chains:
if (type === 'git' || type === 'oci') {
    if (source.hasOwnProperty('chart')) {
        source.path = source.chart;
        delete source.chart;
        source.targetRevision = 'HEAD';
    }
} else if (type === 'helm') {
    if (source.hasOwnProperty('path')) {
        source.chart = source.path;
        delete source.path;
        source.targetRevision = '';
    }
}

// Use switch statement:
switch (type) {
    case 'git':
    case 'oci':
        if ('chart' in source) {
            source.path = source.chart;
            delete source.chart;
            source.targetRevision = 'HEAD';
        }
        break;
    case 'helm':
        if ('path' in source) {
            source.chart = source.path;
            delete source.path;
            source.targetRevision = '';
        }
        break;
}

// Extract complex expressions:
// Instead of inline complex logic:
const selectedApp = apps.find(app => AppUtils.appQualifiedName(app, useAuthSettingsCtx?.appsInAnyNamespaceEnabled) === val);

// Use descriptive temporary variable:
const qualifiedName = AppUtils.appQualifiedName(app, useAuthSettingsCtx?.appsInAnyNamespaceEnabled);
const selectedApp = apps?.find(app => qualifiedName === val);
```