---
title: Handle configuration value changes
description: 'Configuration values should be properly initialized and stay updated
  throughout their lifecycle. Follow these guidelines:


  1. Initialize configuration values immediately upon service creation, not just in
  change handlers:'
repository: microsoft/vscode
label: Configurations
language: TypeScript
comments_count: 4
repository_stars: 174887
---

Configuration values should be properly initialized and stay updated throughout their lifecycle. Follow these guidelines:

1. Initialize configuration values immediately upon service creation, not just in change handlers:
```ts
class ConfigurationAwareService {
  private _configValue: number;
  
  constructor(@IConfigurationService configService: IConfigurationService) {
    // Initialize immediately
    this._configValue = configService.getValue('myConfig');
    
    // Listen for changes
    this._register(configService.onDidChangeConfiguration(e => {
      if (e.affectsConfiguration('myConfig')) {
        this._configValue = configService.getValue('myConfig');
      }
    }));
  }
}
```

2. For frequently accessed configurations, cache the value and update via change events rather than querying on each use:
```ts
// AVOID: Querying on each use
getConfig() {
  return this.configService.getValue('myConfig');
}

// BETTER: Cache and update on changes
private _cachedConfig = this.configService.getValue('myConfig');
getConfig() {
  return this._cachedConfig;
}
```

3. When handling configuration changes, use `affectsConfiguration()` to efficiently check if your configuration was modified before updating cached values.

4. For services that depend on initial configuration state, ensure values are available before service initialization or handle the undefined case appropriately.