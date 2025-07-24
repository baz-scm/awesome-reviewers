---
title: Clear, descriptive identifiers
description: Choose variable, component, and parameter names that clearly describe
  their purpose and avoid ambiguity. Names should fully reflect functionality, be
  properly spelled, and avoid confusion with library terms or similar concepts.
repository: supabase/supabase
label: Naming Conventions
language: TSX
comments_count: 5
repository_stars: 86070
---

Choose variable, component, and parameter names that clearly describe their purpose and avoid ambiguity. Names should fully reflect functionality, be properly spelled, and avoid confusion with library terms or similar concepts.

Good identifiers:
- Are semantic rather than implementation-focused (e.g., use `ProtectedSchemaWarning` instead of `Alert_Shadcn_`)
- Avoid ambiguity with library terminology (e.g., use `isHealthy` instead of `isSuccess` when not related to API request status)
- Fully describe contained functionality (e.g., `BillingCustomerDataDialog` instead of `BillingAddressDialog` when handling both address and tax ID)
- Use correct spelling (e.g., `referral` not `referal`)

Example:
```typescript
// Unclear naming, potential confusion with React Query
const StatusMessage = ({ isSuccess, status }) => {
  if (isSuccess) return 'Healthy'
  // ...
}

// Clear, descriptive naming that avoids ambiguity
const StatusMessage = ({ isHealthy, status }) => {
  if (isHealthy) return 'Healthy'
  // ...
}
```

Clear naming significantly improves code readability, maintainability, and reduces the cognitive load for developers who need to understand the code.