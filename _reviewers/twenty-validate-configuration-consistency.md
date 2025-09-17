---
title: Validate configuration consistency
description: Ensure configuration values have consistent defaults across all systems
  and validate configuration structures using shared schemas. When introducing new
  configuration options, establish system-detected defaults that work intelligently
  based on browser or environment context, similar to existing patterns for date/time
  formats and timezone detection.
repository: twentyhq/twenty
label: Configurations
language: TypeScript
comments_count: 4
repository_stars: 35477
---

Ensure configuration values have consistent defaults across all systems and validate configuration structures using shared schemas. When introducing new configuration options, establish system-detected defaults that work intelligently based on browser or environment context, similar to existing patterns for date/time formats and timezone detection.

Use validation schemas (preferably Zod) that can be shared between frontend, backend, and CLI components to maintain consistency. Support flexible configuration sources through environment variables while maintaining a clear hierarchy of configuration precedence.

Example implementation:
```typescript
// In twenty-shared
export const ConfigSchema = z.object({
  dateFormat: z.enum([DateFormat.MONTH_FIRST, DateFormat.DAY_FIRST]).default(DateFormat.MONTH_FIRST),
  timeFormat: z.enum([TimeFormat.HOUR_12, TimeFormat.HOUR_24]).default(TimeFormat.HOUR_24),
  numberFormat: z.enum([NumberFormat.COMMAS_AND_DOT, NumberFormat.DOTS_AND_COMMA]).default(NumberFormat.COMMAS_AND_DOT),
});

// Ensure consistent defaults across frontend and backend
export const defaultConfig = {
  dateFormat: detectDateFormat(), // System-detected default
  timeFormat: detectTimeFormat(), // System-detected default  
  numberFormat: detectNumberFormat(), // System-detected default
};
```

Always verify that default values match between different parts of the system (e.g., Recoil state defaults should match backend environment variable defaults) to prevent configuration conflicts.