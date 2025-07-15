---
title: Centralize configuration values
description: Store all configuration values in dedicated configuration files rather
  than hardcoding them throughout the application. This makes the codebase more maintainable
  and reduces the need for code changes when configurations change.
repository: kubeflow/kubeflow
label: Configurations
language: TypeScript
comments_count: 5
repository_stars: 15064
---

Store all configuration values in dedicated configuration files rather than hardcoding them throughout the application. This makes the codebase more maintainable and reduces the need for code changes when configurations change.

Key practices:
- Use environment files to store configuration values
- Move hardcoded patterns, URLs, and paths to configuration constants
- Design configuration with future extensibility in mind
- Use environment variables for feature toggles and configurable behavior

**Example - Before:**
```typescript
constructor(private translate: TranslateService) {
  const currentLanguage = this.translate.getBrowserLang();
  const lang = currentLanguage.match(/en|fr/) ? currentLanguage : 'en';
}

constructor(iconRegistry: MatIconRegistry, sanitizer: DomSanitizer) {
  iconRegistry.addSvgIcon('jupyterlab', sanitizer.bypassSecurityTrustResourceUrl('static/assets/jupyterlab-wordmark.svg'));
}
```

**Example - After:**
```typescript
// In environment.ts
export const environment = {
  supportedLanguages: ['en', 'fr'],
  defaultLanguage: 'en',
  assetPaths: {
    jupyterlab: 'static/assets/jupyterlab-wordmark.svg',
  }
};

// In component
constructor(private translate: TranslateService) {
  const currentLanguage = this.translate.getBrowserLang();
  const lang = environment.supportedLanguages.includes(currentLanguage) ? 
    currentLanguage : environment.defaultLanguage;
}

constructor(iconRegistry: MatIconRegistry, sanitizer: DomSanitizer) {
  iconRegistry.addSvgIcon(
    'jupyterlab', 
    sanitizer.bypassSecurityTrustResourceUrl(environment.assetPaths.jupyterlab)
  );
}
```

This approach makes it easier to add new languages or assets without modifying component code, and keeps configuration organized in central locations.
