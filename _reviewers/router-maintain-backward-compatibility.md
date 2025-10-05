---
title: Maintain backward compatibility
description: When evolving APIs, always maintain backward compatibility to avoid breaking
  existing user code. Support both old and new syntax during transition periods, and
  use deprecation warnings to guide users toward new patterns.
repository: TanStack/router
label: API
language: TSX
comments_count: 4
repository_stars: 11590
---

When evolving APIs, always maintain backward compatibility to avoid breaking existing user code. Support both old and new syntax during transition periods, and use deprecation warnings to guide users toward new patterns.

Key practices:
- Use function overloads or runtime type checking to support multiple API signatures
- Add deprecation warnings for old patterns while keeping them functional
- Follow semantic versioning - breaking changes only in major versions
- When changing parameter names or structure, support both old and new formats

Example from useBlocker API evolution:
```tsx
// Support both old and new syntax
export function useBlocker(
  blockerFnOrOpts: BlockerFn | BlockerOpts,
  condition?: boolean | any
): BlockerResolver {
  if (typeof blockerFnOrOpts === 'function') {
    // Legacy function signature
    return useBlockerInternal(blockerFnOrOpts, condition)
  } else {
    // New object-based signature
    return useBlockerInternal(blockerFnOrOpts.blockerFn, blockerFnOrOpts.condition)
  }
}
```

This approach allows gradual migration while preventing immediate breakage for existing users. Always consider the impact on downstream consumers before changing public API surfaces.