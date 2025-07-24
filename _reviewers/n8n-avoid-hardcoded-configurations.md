---
title: Avoid hardcoded configurations
description: Never hardcode environment-specific values or feature states directly
  in your code. Instead, use environment variables, configuration files, or feature
  flag systems to manage these values dynamically.
repository: n8n-io/n8n
label: Configurations
language: Other
comments_count: 2
repository_stars: 122978
---

Never hardcode environment-specific values or feature states directly in your code. Instead, use environment variables, configuration files, or feature flag systems to manage these values dynamically.

For environment URLs:
```javascript
// BAD
window.location.replace('https://stage.ciaraai.com/workflows');

// GOOD
window.location.replace(process.env.VUE_APP_PLATFORM_URL + '/workflows');
```

For feature flags and UI components:
```vue
// BAD
<N8nBadge class="ml-4xs">{{ i18n.baseText('generic.upgrade') }}</N8nBadge>

// GOOD
<N8nBadge v-if="!settingsStore.isEnterpriseFeatureEnabled[EnterpriseEditionFeature.EnforceMFA]" class="ml-4xs">
  {{ i18n.baseText('generic.upgrade') }}
</N8nBadge>
```

Hardcoded configurations are difficult to maintain, lead to environment-specific bugs, and can result in misleading UI elements for users. Always retrieve configuration values from the appropriate source at runtime to ensure your application behaves correctly across all environments and user scenarios.