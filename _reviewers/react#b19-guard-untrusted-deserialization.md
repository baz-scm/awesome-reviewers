---
title: Guard untrusted deserialization
description: When parsing or deserializing data that originates from an untrusted
  source (network payloads, serialized models, user-controlled streams), never blindly
  traverse or merge properties. Explicitly validate object ownership before accessing
  a property (e.g. `hasOwnProperty.call(value, name)`) so inherited or prototype properties
  can't be used to "drill into"...
repository: facebook/react#b19
label: Security
language: JavaScript
comments_count: 3
repository_stars: 251893
---

When parsing or deserializing data that originates from an untrusted source (network payloads, serialized models, user-controlled streams), never blindly traverse or merge properties. Explicitly validate object ownership before accessing a property (e.g. `hasOwnProperty.call(value, name)`) so inherited or prototype properties can't be used to "drill into" objects that weren't created by the parser itself — this closes prototype-pollution/gadget-style attacks. Prefer constructing plain objects with a `null` prototype for parsed data when possible, to avoid needing ad-hoc ownership checks scattered across every traversal site.

Also enforce symmetry between what is serialized and what is deserialized: if a field is only ever produced in one environment (e.g. `Error.cause`/`AggregateError.errors` only serialized in `__DEV__`), guard the corresponding deserialization code with the same condition so production code never processes data it could not have legitimately received. This acts as defense-in-depth even if the serializer behavior changes unexpectedly.

Finally, when combining or merging resources that carry security-relevant metadata (such as CSP `nonce` values on styles/scripts), never merge entries whose security attributes differ. Determine the security context (e.g. nonce) once, as early as possible, and treat it as authoritative for all related entries; reject or avoid merging contributions that supply a conflicting value rather than silently combining them, since doing so could weaken or bypass the intended security policy.

Example:
```js
// Bad: trusts any property, including inherited ones
if (typeof value === 'object' && name in value) { ... }

// Good: only trusts the object's own properties
if (typeof value === 'object' && hasOwnProperty.call(value, name)) { ... }

// Good: deserialization mirrors serialization constraints
const errorOptions =
  __DEV__ && 'cause' in errorInfo ? {cause: errorInfo.cause} : {};
```</description>
</invoke>
