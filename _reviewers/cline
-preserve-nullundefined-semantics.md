---
title: Preserve null/undefined semantics
description: Null, undefined, and empty values often encode distinct domain meanings
  (e.g. "clear this field" vs "omit/keep unchanged" vs "use default" vs "empty but
  present"). Bugs creep in whenever these are collapsed through shortcuts that don't
  respect the intended semantics. Before using `??`, truthy checks, or spread/serialize
  helpers on a nullable value, confirm...
repository: 'cline/cline

  '
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 70942
---

Null, undefined, and empty values often encode distinct domain meanings (e.g. "clear this field" vs "omit/keep unchanged" vs "use default" vs "empty but present"). Bugs creep in whenever these are collapsed through shortcuts that don't respect the intended semantics. Before using `??`, truthy checks, or spread/serialize helpers on a nullable value, confirm what each state is supposed to mean end-to-end, and verify every layer (parsing, encoding, storage) preserves that distinction.

Concretely:
- Don't use `??` when an empty-but-defined value (e.g. `[]`) should still trigger a fallback. Prefer an explicit check such as `images?.length ? images : retry.images` instead of `images ?? retry.images`.
- When a field supports an explicit "clear" semantic (e.g. `metadata: null`), make sure serialization doesn't silently turn it into "omitted" (e.g. encoding `null` as `{}` if that's what downstream decoders expect as "no value provided").
- Keep type signatures honest about what values actually flow through the code: if a parameter's default only swallows `undefined`, don't type it as accepting `undefined` when the real sentinel is `null` (and vice versa) — mismatches here let unintended fallback values slip through.
- Don't let a value fall through to a destructive path (e.g. replacing a live session) just because a null/undefined check didn't match the rare case; fail loudly (throw) rather than silently continuing when an invariant you depend on turns out false.

When designing new nullable fields, prefer initializing non-nullable defaults over introducing optional/nullable state if the nullable path is rarely meaningful — this removes a whole class of these bugs by construction.