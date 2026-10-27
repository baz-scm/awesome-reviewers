---
title: Untrusted data validation
description: When code traverses or merges data that originates from an untrusted
  or externally-controlled source (deserialized payloads, user-supplied options, CSP
  nonces, etc.), never assume the data is safe to use as-is — explicitly validate
  the trust boundary before acting on it.
repository: facebook/react#b20
label: Security
language: JavaScript
comments_count: 3
repository_stars: 251895
---

When code traverses or merges data that originates from an untrusted or externally-controlled source (deserialized payloads, user-supplied options, CSP nonces, etc.), never assume the data is safe to use as-is — explicitly validate the trust boundary before acting on it.

- For deserialization/traversal code, guard every property access with an own-property check (e.g. `hasOwnProperty`) so that prototype-chain gadgets (`__proto__`, inherited methods, etc.) can't be exploited to read or write properties the parser never created:
```js
if (typeof value === 'object' && hasOwnProperty.call(value, name)) {
  // safe to access value[name]
}
```
Prefer constructing objects with a `null` prototype (or `Object.create(null)`) when building the parsed result, so you don't need to scatter these guards at every traversal site ("shotgun surgery").

- For security tokens such as CSP nonces, don't silently merge or infer values across independently-provided inputs. If two resources (e.g. style rules merged into one `<style>` tag) could carry different nonces, either require the nonce to be established once at creation time and reused consistently, or add explicit validation/dev warnings when mismatched values are detected, rather than letting one arbitrary value win. Avoid auto-generating or auto-applying security tokens on behalf of the user — require them to be passed explicitly so the author retains control and the behavior isn't a false sense of protection.

Applying this standard means every place where trust crosses a boundary (deserialized object graph, merged resources, security tokens) has an explicit, auditable check rather than an implicit assumption.