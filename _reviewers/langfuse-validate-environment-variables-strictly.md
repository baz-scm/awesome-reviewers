---
title: Validate environment variables strictly
description: Implement comprehensive validation for environment variables using a
  schema validation library (e.g., Zod). Include proper typing, conditional validation
  rules, and sensible defaults. This ensures configuration errors are caught early
  and prevents runtime issues.
repository: langfuse/langfuse
label: Configurations
language: TypeScript
comments_count: 3
repository_stars: 13574
---

Implement comprehensive validation for environment variables using a schema validation library (e.g., Zod). Include proper typing, conditional validation rules, and sensible defaults. This ensures configuration errors are caught early and prevents runtime issues.

Key practices:
1. Use strong typing for environment variables
2. Implement conditional validation for dependent configs
3. Provide clear fallback values where appropriate

Example:
```typescript
const EnvSchema = z.object({
  // Use appropriate types instead of string enums
  DEBUG_MODE: z.coerce.boolean().default(false),
  
  // Add conditional validation for dependent configs
  S3_MEDIA_UPLOAD_SSE: z.enum(["AES256", "aws:kms"]).optional(),
  S3_MEDIA_UPLOAD_KMS_KEY_ID: z.string().optional()
    .refine((val, ctx) => {
      if (ctx.parent.S3_MEDIA_UPLOAD_SSE === "aws:kms" && !val) {
        return false;
      }
      return true;
    }, "KMS key ID required when using aws:kms encryption"),

  // Provide fallbacks for optional configs
  SENTRY_RELEASE: z.string().optional()
    .default(process.env.BUILD_ID ?? "unknown")
});
```