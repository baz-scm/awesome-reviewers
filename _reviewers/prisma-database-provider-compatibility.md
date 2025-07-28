---
title: Database provider compatibility
description: Ensure database code properly handles provider-specific differences and
  capabilities. Different database providers have varying syntax requirements, feature
  support, and connection methods that must be accounted for in the implementation.
repository: prisma/prisma
label: Database
language: TypeScript
comments_count: 7
repository_stars: 42967
---

Ensure database code properly handles provider-specific differences and capabilities. Different database providers have varying syntax requirements, feature support, and connection methods that must be accounted for in the implementation.

Key areas to consider:
- **Parameter binding**: Some databases use numbered parameters (`$1`, `$2`) while others use anonymous placeholders (`?`)
- **Feature availability**: Certain features like transaction isolation levels may only be available for specific providers (e.g., "this is really only available for SQL servers")
- **Connection methods**: Different providers support different connection approaches (TCP, Unix sockets, etc.)
- **Data types**: Column type mapping varies between providers and may depend on additional flags
- **Schema generation**: Default schemas must be valid for the target provider

Example of proper provider-specific handling:
```typescript
// Handle parameter binding differences
const usesAnonymousParams = [Providers.MYSQL, Providers.SQLITE].includes(provider)

// Skip provider-specific features appropriately  
if (datasource.provider !== 'sqlite' && parseEnvValue(datasource.url) === defaultURL(datasource.provider)) {
  // Show warning for non-SQLite providers only
}

// Handle provider-specific connection methods
if (credentials.type === 'postgresql' || credentials.type === 'cockroachdb') {
  // Unix socket handling for PostgreSQL-compatible databases
}
```

Always test provider-specific code paths and avoid making assumptions about universal database feature support.