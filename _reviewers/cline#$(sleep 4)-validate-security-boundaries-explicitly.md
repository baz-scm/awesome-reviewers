---
title: Validate security boundaries explicitly
description: 'Never trust implicit assumptions when a value crosses a security boundary:
  validate it explicitly at the point of use rather than relying on cached state,
  plain object lookups, or approximate documentation.'
repository: cline/cline#$(sleep 4)
label: Security
language: TSX
comments_count: 3
repository_stars: 70978
---

Never trust implicit assumptions when a value crosses a security boundary: validate it explicitly at the point of use rather than relying on cached state, plain object lookups, or approximate documentation.

1. When indexing a plain JavaScript object with a key that can be influenced by external input (file names, paths, user-provided strings), guard the lookup with `Object.hasOwn(table, key)` (or use a `Map`) before returning the value. Otherwise an attacker-chosen key like `"constructor"`, `"__proto__"`, or `"toString"` resolves to an inherited prototype property instead of `undefined`, which can lead to prototype-pollution style bugs.

```ts
function lookupIcon(table: Record<string, IconSpec>, key: string): IconSpec | undefined {
	return Object.hasOwn(table, key) ? table[key] : undefined;
}
```

2. Do not treat cached or locally-stored state (e.g., a workspace manifest, a feature flag, an "eligibility" flag computed earlier) as an authorization decision. Any action that grants access to a resource (publishing, running a privileged command, etc.) must re-validate the actual permission/state at the time the action executes, even if cached data is used to improve UX by gating the UI earlier.

3. When describing a security/sandboxing boundary to users (e.g., settings descriptions), be precise about what is actually enforced versus what is merely possible. If file reads are unrestricted but command execution is sandboxed to the project directory, say so explicitly rather than using language that implies a different or broader protection than what is enforced.

Applying these checks consistently prevents prototype-pollution-class bugs, stale-authorization bypasses, and user confusion about the actual security guarantees of a feature.