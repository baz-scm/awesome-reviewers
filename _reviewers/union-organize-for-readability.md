---
title: organize for readability
description: Structure code to minimize repetition and improve clarity through appropriate
  abstraction and import organization. When code contains repetitive patterns, create
  wrapper functions to eliminate boilerplate. For modules with structured exports
  (like ADTs), prefer qualified imports over individual named imports to maintain
  clear namespace organization.
repository: unionlabs/union
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 74800
---

Structure code to minimize repetition and improve clarity through appropriate abstraction and import organization. When code contains repetitive patterns, create wrapper functions to eliminate boilerplate. For modules with structured exports (like ADTs), prefer qualified imports over individual named imports to maintain clear namespace organization.

Example of abstracting repetitive patterns:
```typescript
// Instead of repeating tryPromise wrapping:
const amount = yield* Effect.tryPromise({
  try: () => client.getBalance(minter, "uxion"),
  catch: e => new Error(`Failed to fetch balance: ${String(e)}`)
})

// Create wrapper functions:
const getBalance = (address: string, denom: string) => 
  Effect.tryPromise({
    try: () => client.getBalance(address, denom),
    catch: e => new Error(`Failed to fetch balance: ${String(e)}`)
  })

// Then use: yield* getBalance(minter, "uxion")
```

Example of qualified imports for structured modules:
```typescript
// Instead of:
import { Batch, Forward, FungibleAssetOrder, Multiplex } from "../src/ucs03/instruction.js"

// Use qualified import:
import * as Instruction from "../src/ucs03/instruction.js"
```

This approach reduces visual clutter, makes the code's intent clearer, and creates more maintainable examples and implementations.