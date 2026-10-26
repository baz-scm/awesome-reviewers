---
title: Safe, explicit API contracts
description: 'Design API surfaces so consumers can’t accidentally use the wrong environment
  or omit critical parameters.


  **Apply this as a standard:**

  1. **Separate incompatible environments** (browser vs server) into **distinct entrypoints/modules**
  when behavior/required globals differ.'
repository: facebook/react#b1
label: API
language: JavaScript
comments_count: 6
repository_stars: 251878
---

Design API surfaces so consumers can’t accidentally use the wrong environment or omit critical parameters.

**Apply this as a standard:**
1. **Separate incompatible environments** (browser vs server) into **distinct entrypoints/modules** when behavior/required globals differ.
2. **Fail fast for server-only concepts in client contexts**: don’t “no-op” server-only exports—throw or otherwise make invalid imports/usages surface immediately in client builds.
3. **Use explicit option shapes**:
   - Prefer an **options bag** over positional/overloaded parameters when tooling/consumers validate inputs via schemas.
   - Make fields that must be forwarded (e.g., integrity/nonce/fetchPriority) **required in the API that performs forwarding**, so missing forwarding is caught by types/review.
4. **Avoid mode-parameter explosions**: if behavior meaningfully diverges, **split into separate functions/variants** rather than adding many optional parameters that are hard to reason about.

**Example patterns (TypeScript-ish):**
```ts
// 1) Required forwarding fields in internal host dispatch
type PreloadImplOptions = {
  integrity?: string,
  fetchPriority?: 'low' | 'auto' | 'high',
  nonce?: string,
};

// Make forwarding safe: the dispatcher expects the full shape.
function preloadModuleImpl(href: string, options?: Required<PreloadImplOptions>) {
  // ensures options.integrity/fetchPriority/nonce are handled intentionally
}

// 2) Client should not be able to import server-only helpers
// Prefer an error (or build-time exclusion) instead of a no-op.
export function addToLedger() {
  throw new Error('addToLedger is server-only');
}

// 3) Options bag for schema-driven consumers
type ToolArgs = { uid: string, includeHooks?: boolean };
function getComponentByUid(args: ToolArgs) {
  // matches a validated input schema
}

// 4) Split variants instead of one multi-mode signature
function createResponseStateForWithFallback(/*...*/) { /*...*/ }
function createResponseState(/*...*/) { /*...*/ }
```

Following this standard reduces runtime surprises (wrong-environment usage, missing forwarded options) and keeps API signatures understandable over time.