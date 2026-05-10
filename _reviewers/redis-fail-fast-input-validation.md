---
title: Fail Fast Input Validation
description: 'Apply a single security rule: validate arity, lengths, ranges, and invariants
  before using inputs to index arrays, dereference pointers, compute derived pointers,
  or persist/serialize into security-sensitive targets.'
repository: redis/redis
label: Security
language: C
comments_count: 8
repository_stars: 74261
---

Apply a single security rule: validate arity, lengths, ranges, and invariants before using inputs to index arrays, dereference pointers, compute derived pointers, or persist/serialize into security-sensitive targets.

Practical checklist:
- **Before argv/key extraction:** verify command arity so helpers can’t read `argv` out of bounds.
- **Before pointer math / derived references:** assert required preconditions (e.g., “the requested metadata bit is set”) before computing offsets.
- **Before dereferencing/freeing-lifetime assumptions:** compute any needed properties (e.g., length) before freeing buffers; don’t call methods on freed objects.
- **Before persisting user-controlled strings into config/protocol text:** either reject dangerous characters (e.g., control chars) or rely on a known escaping layer—don’t do “partial” safety.
- **Before auth/security state changes:** validate security-sensitive parameters (e.g., password policy/length) and keep logging/redaction rules.

Example (arity defense-in-depth):
```c
// In an ACL permission path that inspects argv for keys/channels
if (!commandCheckArity(cmd, argc, NULL)) {
    if (idxptr) *idxptr = 0;
    return ACL_DENIED_CMD;
}

// Also keep boundary checks in shared key-extraction helpers,
// even if callers already validated.
```

Example (invariant assertion before derived pointer):
```c
serverAssert(metaId < KEY_META_ID_MAX && (bits & (1u << metaId)));
```

Example (string control-char validation at persistence boundary):
```c
if (sentinelStringContainsControlChars(val->ptr, sdslen(val->ptr))) {
    addReplyError(c, "value must not contain control characters");
    goto bad;
}
```