---
title: Validate untrusted input strictly
description: Treat any value that originates from user input, HTTP headers, or caller-supplied
  options as untrusted, and validate it with explicit, narrow rules rather than loose
  type checks. Prefer allow-lists or numeric ranges over single-type checks (e.g.
  reject any statusCode outside 100-999 instead of only checking `typeof === 'bigint'`),
  and only trust headers...
repository: Expressjs/Express
label: Security
language: JavaScript
comments_count: 4
repository_stars: 69580
---

Treat any value that originates from user input, HTTP headers, or caller-supplied options as untrusted, and validate it with explicit, narrow rules rather than loose type checks. Prefer allow-lists or numeric ranges over single-type checks (e.g. reject any statusCode outside 100-999 instead of only checking `typeof === 'bigint'`), and only trust headers like `X-Forwarded-For` when the app has explicitly opted in (e.g. `trust proxy` is set), otherwise spoofed values can bypass security logic.

When merging caller-supplied options into security-sensitive defaults (cookies, session config, etc.), make sure those options cannot silently override the security-critical fields. Set the critical values after the merge so they can't be clobbered:

```js
var opts = merge({ path: '/' }, options);
// Force expiration regardless of caller-supplied values
opts.expires = new Date(1);
opts.maxAge = 0;
```

For cryptographic operations (hashing, salting, encryption), follow correct primitives: salts must be unique per user/record, never hard-coded or constant, and any accompanying code comments/documentation must accurately reflect what the code does so reviewers and future maintainers aren't misled about the security guarantees provided.</description>
