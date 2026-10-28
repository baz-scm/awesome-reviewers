---
title: Validate untrusted input and authorization
description: Never trust client-supplied or cached data as the basis for a security
  decision, and never use untrusted strings directly as object property keys. For
  authorization-sensitive actions (e.g., enabling a command that requires an external
  connection or permission), perform a live check against the authoritative source
  at the time of use rather than gating only...
repository: "cline/cline\r\n"
label: Security
language: TSX
comments_count: 2
repository_stars: 70946
---

Never trust client-supplied or cached data as the basis for a security decision, and never use untrusted strings directly as object property keys. For authorization-sensitive actions (e.g., enabling a command that requires an external connection or permission), perform a live check against the authoritative source at the time of use rather than gating only on a feature flag or a potentially stale cached value; cached state can inform UX hints, but must never substitute for a real-time authorization check.

Similarly, when building lookup tables keyed by arbitrary or user/file-derived strings (extensions, filenames, folder names, etc.), avoid plain `obj[key]` access, since keys like `"constructor"`, `"__proto__"`, or `"toString"` can resolve to inherited `Object.prototype` members instead of `undefined`, leading to prototype-pollution-style bugs or security issues. Guard every dynamic lookup with `Object.hasOwn(obj, key)` (or `Object.prototype.hasOwnProperty.call`) before returning the mapped value, and add a regression test covering keys such as `constructor`, `__proto__`, and `toString`.

Example:
```ts
function fileIconSpec(path: string): IconSpec {
	const name = baseName(path).toLowerCase();
	if (Object.hasOwn(BY_NAME, name)) return BY_NAME[name];
	const ext = extname(name);
	if (Object.hasOwn(BY_EXTENSION, ext)) return BY_EXTENSION[ext];
	return DEFAULT_ICON;
}
```

Apply this standard whenever (a) a feature exposes an action gated by permissions/connections, or (b) code indexes into a plain object/map using a key derived from user input, file paths, or any external source.