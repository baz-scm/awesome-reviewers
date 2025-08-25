---
title: Use configuration enums
description: Replace hardcoded string matching and magic values with proper configuration
  enums or flags. This improves maintainability, reduces errors, and makes configuration
  behavior explicit and type-safe.
repository: block/goose
label: Configurations
language: TSX
comments_count: 2
repository_stars: 19037
---

Replace hardcoded string matching and magic values with proper configuration enums or flags. This improves maintainability, reduces errors, and makes configuration behavior explicit and type-safe.

Instead of checking string content for configuration decisions:
```typescript
// Avoid: hardcoded string matching
{!prompt?.includes('SECURITY WARNING') && (
  <Button onClick={() => handleButtonClick(ALWAYS_ALLOW)}>
    Always Allow
  </Button>
)}
```

Use explicit configuration enums or flags:
```typescript
// Better: explicit configuration enum
enum ConfirmationType {
  STANDARD = 'standard',
  SECURITY_WARNING = 'security_warning',
  CRITICAL = 'critical'
}

{confirmationType !== ConfirmationType.SECURITY_WARNING && (
  <Button onClick={() => handleButtonClick(ALWAYS_ALLOW)}>
    Always Allow
  </Button>
)}
```

Similarly, for platform-specific configurations, use structured approaches rather than inline conditionals. This pattern prevents bugs from typos in string matching, makes the configuration intent clear to other developers, and enables better tooling support through TypeScript's type system.