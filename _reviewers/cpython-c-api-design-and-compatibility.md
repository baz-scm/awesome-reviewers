---
title: C API design and compatibility
description: When adding or extending a public C API (including the limited/stable
  ABI), design signatures and semantics to match established conventions used elsewhere
  in the ecosystem, and keep documentation perfectly in sync with the actual implementation
  (e.g., don't document a `size` parameter that doesn't exist yet in the function
  signature). For functions that...
repository: python/cpython
label: API
language: Other
comments_count: 4
repository_stars: 77696
---

When adding or extending a public C API (including the limited/stable ABI), design signatures and semantics to match established conventions used elsewhere in the ecosystem, and keep documentation perfectly in sync with the actual implementation (e.g., don't document a `size` parameter that doesn't exist yet in the function signature). For functions that have known analogues in other widely-used libraries (e.g., `isprime` vs. gmpy2's probabilistic `is_probab_prime`), explicitly consider and document compatibility expectations so the new API can be used as a drop-in replacement or its differences are clearly called out.

When exposing or checking capsule-based or versioned C APIs, prefer minimal, robust compatibility checks (e.g., magic number and struct size) over strict version-number matching, since exact version checks may be incorrect assumptions for third-party consumers and can unnecessarily break compatibility.

Any change that adds, removes, or modifies a symbol in the limited API must be accompanied by the required bookkeeping: update `Misc/stable_abi.txt` and run `make regen-limited-abi` so the stable ABI manifest stays accurate.

Example checklist before merging a new/extended C API:
1. Does the function signature match what's documented?
2. Does it follow naming/parameter conventions used by similar existing APIs (both internal and in the broader ecosystem)?
3. If used for capability detection, are checks (magic/size) minimal and robust rather than overly strict (e.g., avoid exact version equality checks)?
4. If part of the limited API, has `Misc/stable_abi.txt` been updated and `make regen-limited-abi` been run?