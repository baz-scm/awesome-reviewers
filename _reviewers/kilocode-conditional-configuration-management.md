---
title: Conditional configuration management
description: Ensure configurations are conditional, context-aware, and resilient.
  Use feature flags to control functionality availability rather than instructing
  systems to avoid certain features. Implement proper fallbacks for missing configuration
  values and support backward compatibility when introducing new config formats.
repository: kilo-org/kilocode
label: Configurations
language: TypeScript
comments_count: 8
repository_stars: 7302
---

Ensure configurations are conditional, context-aware, and resilient. Use feature flags to control functionality availability rather than instructing systems to avoid certain features. Implement proper fallbacks for missing configuration values and support backward compatibility when introducing new config formats.

Key practices:
- Use feature flags to conditionally include/exclude tools and functionality
- Provide sensible fallbacks for missing configuration values  
- Support multiple configuration formats for backward compatibility
- Make hardcoded values configurable when they may need to vary by context
- Handle configuration errors gracefully with clear error messages

Example:
```typescript
// Good: Conditional tool availability based on feature flag
if (experiments?.morphFastApply !== true) {
    tools.delete("edit_file")
}

// Good: Fallback to system language instead of hardcoded default
initializeI18n(context.globalState.get("language") ?? formatLanguage(vscode.env.language))

// Good: Support multiple rule file formats for backward compatibility  
const ruleFiles = [".kilocoderules", ".roorules", ".clinerules"]

// Good: Make hardcoded values configurable
const sizeLimit = config.get("sizeLimitFraction") ?? SIZE_LIMIT_AS_CONTEXT_WINDOW_FRACTION
```