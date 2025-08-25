---
title: Avoid hardcoded configuration values
description: Extract hardcoded configuration values into constants, environment variables,
  or function parameters to improve maintainability and flexibility. Magic numbers,
  provider names, file size limits, and other configuration values should not be embedded
  directly in business logic.
repository: calcom/cal.com
label: Configurations
language: TypeScript
comments_count: 3
repository_stars: 37732
---

Extract hardcoded configuration values into constants, environment variables, or function parameters to improve maintainability and flexibility. Magic numbers, provider names, file size limits, and other configuration values should not be embedded directly in business logic.

Examples of what to avoid:
```typescript
// Bad: Hardcoded provider name
const newNumber = await prisma.calAiPhoneNumber.create({
  data: {
    provider: "retell", // Hardcoded provider
    // ...
  }
});

// Bad: Magic numbers
const creditMultiplier = team.isOrganization ? 0.2 : 0.5; // Magic numbers

// Bad: Hardcoded file size limit
if (file.size > MAX_IMAGE_FILE_SIZE) { // Hardcoded constant
```

Better approaches:
```typescript
// Good: Get provider from service response
const provider = retellPhoneNumber.provider || "retell";

// Good: Use named constants or environment variables
const ORG_CREDIT_MULTIPLIER = 0.2;
const TEAM_CREDIT_MULTIPLIER = 0.5;
const creditMultiplier = team.isOrganization ? ORG_CREDIT_MULTIPLIER : TEAM_CREDIT_MULTIPLIER;

// Good: Make limits configurable
export const validateImageFile = async (
  file: File, 
  maxFileSize: number, // Accept as parameter
  t: (key: string) => string
): Promise<boolean> => {
  if (file.size > maxFileSize) {
```

This approach makes code more testable, allows for environment-specific configurations, and reduces the risk of inconsistencies when the same values are used in multiple places.