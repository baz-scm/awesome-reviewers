---
title: Centralize configuration management
description: Extract configuration state, feature flags, and version-dependent settings
  into dedicated services rather than hardcoding values or prop drilling through component
  hierarchies. This approach improves maintainability, testability, and allows for
  easier updates without code changes.
repository: angular/angular
label: Configurations
language: Html
comments_count: 2
repository_stars: 98611
---

Extract configuration state, feature flags, and version-dependent settings into dedicated services rather than hardcoding values or prop drilling through component hierarchies. This approach improves maintainability, testability, and allows for easier updates without code changes.

For global settings, use a centralized service:
```typescript
// Instead of prop drilling
[signalGraphEnabled]="signalGraphEnabled()"
(showSignalGraph)="showSignalGraph.emit($event)"

// Use a settings service
@Injectable()
export class SettingsService {
  signalGraphEnabled = signal(false);
  // Other configuration properties
}
```

For version-dependent features, avoid hardcoded version strings:
```typescript
// Instead of hardcoded versions
"Angular applications using version 21 and greater"

// Use configurable version requirements
"Angular applications using version {{minVersion}} and greater"
```

This pattern prevents configuration from being scattered across components and makes it easier to manage environment-specific settings, feature toggles, and version requirements from a single source of truth.