---
title: JSDoc documentation standards
description: All public functions and complex code should have proper JSDoc documentation.
  Functions must include clear descriptions of their purpose, parameters, and return
  values. Ensure JSDoc comments are accurate, well-formatted, and kept up-to-date
  with code changes.
repository: cloudflare/workers-sdk
label: Documentation
language: TypeScript
comments_count: 5
repository_stars: 3379
---

All public functions and complex code should have proper JSDoc documentation. Functions must include clear descriptions of their purpose, parameters, and return values. Ensure JSDoc comments are accurate, well-formatted, and kept up-to-date with code changes.

For JSDoc formatting:
- Use backticks around code references like `worker-configuration.d.ts`
- Keep descriptions concise but complete
- Update documentation when functionality changes

Example of proper JSDoc:
```typescript
/**
 * Unified function to handle binding name validation, prompting, and config updates
 * for all resource creation commands. This eliminates code duplication across
 * KV, D1, R2, Vectorize, and Hyperdrive commands.
 *
 * @param args - Configuration arguments including optional binding name and environment
 * @param config - Raw configuration object with optional config path
 * @param resource - Resource binding information
 */
export async function handleResourceBindingAndConfigUpdate(
	args: { configBindingName?: string; env?: string },
	config: RawConfig & { configPath?: string },
	resource: ResourceBinding
): Promise<void>
```

Additionally, add explanatory comments for non-obvious code logic, complex algorithms, or when the purpose isn't immediately clear from the code itself.