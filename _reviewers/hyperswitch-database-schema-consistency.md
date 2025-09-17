---
title: Database schema consistency
description: Ensure database schema definitions are consistent with ORM annotations
  and include proper constraints for data integrity and security. This includes matching
  primary key definitions between migrations and ORM models, making foreign key relationships
  mandatory where appropriate, and requiring tenant identifiers in queries to prevent
  cross-tenant data access.
repository: juspay/hyperswitch
label: Database
language: Rust
comments_count: 4
repository_stars: 34028
---

Ensure database schema definitions are consistent with ORM annotations and include proper constraints for data integrity and security. This includes matching primary key definitions between migrations and ORM models, making foreign key relationships mandatory where appropriate, and requiring tenant identifiers in queries to prevent cross-tenant data access.

Key practices:
1. **Primary key consistency**: Verify that Diesel annotations match SQL migration primary key definitions
2. **Mandatory relationships**: Make foreign keys non-nullable when they represent required relationships
3. **Tenant isolation**: Always include merchant_id or similar tenant identifiers in queries for multi-tenant security

Example issues to avoid:
```rust
// ❌ Primary key mismatch
#[diesel(primary_key(id))]  // Only 'id' specified
// But SQL migration has: PRIMARY KEY (id, created_at)

// ❌ Nullable foreign key that should be mandatory
subscription_id -> Nullable<Varchar>,  // Should be required

// ❌ Query without tenant isolation
async fn find_by_id(id: String) -> Result<Entity> {
    // Missing merchant_id constraint - security risk
}

// ✅ Correct implementations
#[diesel(primary_key(id, created_at))]  // Matches migration

subscription_id -> Varchar,  // Mandatory relationship

async fn find_by_merchant_id_and_id(
    merchant_id: &MerchantId, 
    id: String
) -> Result<Entity> {
    // Proper tenant isolation
}
```

This ensures data integrity, prevents security vulnerabilities, and maintains consistency between database schema and application code.