---
title: Environment variable patterns
description: Use consistent patterns for environment variable handling and configuration
  validation. Access environment variables directly where they're needed rather than
  loading them unnecessarily in build configurations. Provide clear fallback mechanisms
  and fail fast with descriptive error messages when required configuration is missing
  or invalid.
repository: rocicorp/mono
label: Configurations
language: TypeScript
comments_count: 6
repository_stars: 2091
---

Use consistent patterns for environment variable handling and configuration validation. Access environment variables directly where they're needed rather than loading them unnecessarily in build configurations. Provide clear fallback mechanisms and fail fast with descriptive error messages when required configuration is missing or invalid.

Key practices:
- Access `process.env` directly in the consuming module instead of loading environment variables in build/config files
- Use environment variables instead of hard-coded paths: prefer `ZERO_SCHEMA_PATH=shared/schema.ts` over hard-coding paths
- Implement proper fallback chains with validation:

```typescript
const loadSchemaJson = () => {
  if (process.env.ZERO_SCHEMA_JSON) {
    return process.env.ZERO_SCHEMA_JSON;
  }
  
  try {
    const schema = readFileSync("zero-schema.json", "utf8");
    return JSON.stringify(JSON.parse(schema));
  } catch (error) {
    throw new Error(
      "Schema must be provided via ZERO_SCHEMA_JSON env var or zero-schema.json file"
    );
  }
};
```

- Fail fast on configuration conflicts rather than issuing warnings that may be ignored
- Add new environment variables to `.env.example` files for documentation
- Validate configuration values early in the application lifecycle with clear error messages