---
title: Provide configuration fallbacks
description: Always provide sensible default or fallback values for configuration
  properties to prevent undefined states that can block users or cause application
  errors. Configuration properties should never be left in an undefined state that
  prevents normal application functionality.
repository: cline/cline
label: Configurations
language: TSX
comments_count: 3
repository_stars: 48299
---

Always provide sensible default or fallback values for configuration properties to prevent undefined states that can block users or cause application errors. Configuration properties should never be left in an undefined state that prevents normal application functionality.

When defining configuration properties, especially those that come from external sources (servers, user settings, migrations), include appropriate fallback values using logical OR operators or default parameter values.

Example of proper fallback implementation:
```typescript
// Good: Provides fallback to prevent undefined state
const selectedProvider = 
    (currentMode === "plan" ? apiConfiguration?.planModeApiProvider : apiConfiguration?.actModeApiProvider) || "cline"

// Good: Default parameter with fallback URL
const CreditLimitError: React.FC<CreditLimitErrorProps> = ({
    buyCreditsUrl = "https://api.cline.bot/dashboard/account?tab=credits&redirect=true",
    // other props...
}) => {

// Good: Explicit default value to prevent UI flashing
const defaultState = {
    welcomeViewCompleted: false, // Default to show welcome unless overridden
    // other defaults...
}
```

This practice is especially critical for:
- API provider configurations that may not be set during initial setup or failed migrations
- URL configurations that serve as fallbacks when server values are unavailable  
- Boolean flags that control UI state and should have explicit default behavior
- Any configuration that could cause the application to become unusable if undefined

The fallback values should represent the most sensible default behavior for new users or error recovery scenarios.