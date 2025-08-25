---
title: validate business logic constraints
description: Before adding database constraints or designing schema relationships,
  thoroughly understand the underlying business logic and data relationships. Constraints
  that seem logical at first glance may break existing functionality or prevent valid
  use cases.
repository: calcom/cal.com
label: Database
language: Prisma
comments_count: 3
repository_stars: 37732
---

Before adding database constraints or designing schema relationships, thoroughly understand the underlying business logic and data relationships. Constraints that seem logical at first glance may break existing functionality or prevent valid use cases.

Key practices:
- Research existing code to understand how data is actually used before adding unique constraints
- Consider future extensibility when designing schemas - use discriminator fields instead of separate optional columns
- Validate that proposed constraints align with actual business requirements, not just theoretical data integrity

Example from schema design:
```prisma
// Instead of separate optional fields for different credit types:
model CreditExpenseLog {
  smsSegments     Int?
  callDuration    Int?
  // Consider a more extensible approach:
  creditFor       String  // "SMS", "CALL", etc.
  amount          Int
  metadata        Json?   // Store type-specific data
}
```

This approach prevents constraint conflicts like `@@unique([outlookSubscriptionId, eventTypeId])` when the same subscription ID is legitimately reused across multiple event types, and makes the schema more maintainable as new credit types are added.