---
title: use Effect Option consistently
description: Replace null, undefined, and error throwing with Effect's Option type
  for handling potentially missing values. This provides better type safety, composability,
  and prevents null reference errors.
repository: unionlabs/union
label: Null Handling
language: TypeScript
comments_count: 3
repository_stars: 74800
---

Replace null, undefined, and error throwing with Effect's Option type for handling potentially missing values. This provides better type safety, composability, and prevents null reference errors.

Instead of returning null:
```typescript
// ❌ Avoid
getBannerForEdition(edition: "app" | "btc"): BannerConfig | null {
  // ...
}

// ✅ Prefer
getBannerForEdition(edition: "app" | "btc"): Option.Option<BannerConfig> {
  // ...
}
```

Instead of using undefined:
```typescript
// ❌ Avoid  
address = $state<Hex | undefined>(undefined)

// ✅ Prefer
address = $state<Option.Option<Hex>>(Option.none())
```

Instead of throwing errors for missing values:
```typescript
// ❌ Avoid
export function evmDisplayToCanonical(displayAddress: string): Uint8Array {
  if (!/^0x[0-9a-fA-F]{40}$/.test(displayAddress)) {
    throw new Error("EVM address must be 0x followed by 40 hex characters")
  }
  // ...
}

// ✅ Prefer  
export function evmDisplayToCanonical(displayAddress: AddressEvmDisplay): Option.Option<AddressCanonicalBytes> {
  // validation handled by schema, return Option for safety
  // ...
}
```

Option provides a composable API with methods like `map`, `flatMap`, and `getOrElse` that make handling optional values more explicit and less error-prone than null checks.