---
title: Preserve protocol semantics
description: Network/HTTP code must strictly respect protocol contracts and avoid
  silent behavioral changes. When parsing values governed by an RFC grammar (e.g.
  Content-Length or chunk-size), validate against that grammar before handing them
  to a more permissive parser like `int()`, so unintended inputs (signs, underscores,
  `0x` prefixes, etc.) aren't accepted as...
repository: python/cpython
label: Networking
language: Python
comments_count: 4
repository_stars: 77696
---

Network/HTTP code must strictly respect protocol contracts and avoid silent behavioral changes. When parsing values governed by an RFC grammar (e.g. Content-Length or chunk-size), validate against that grammar before handing them to a more permissive parser like `int()`, so unintended inputs (signs, underscores, `0x` prefixes, etc.) aren't accepted as valid. When transforming or retrying a request, never implicitly alter protocol-level behavior the caller relied on: e.g. don't swap a `Content-Length`-framed body for a chunked-encoded iterator just to make it re-readable, since some servers reject chunked uploads; and don't change the data type of transferred bytes (e.g. yielding `str` chunks from a text-mode file where `bytes` are expected), mirroring how existing code (such as `http.client`) already encodes such chunks. If a known protocol quirk or third-party bug causes a test to need special-casing (e.g. suppressing an exception), don't silently swallow it—assert the actual observed behavior and add a comment/doc note explaining the root cause and linking the upstream issue, so the workaround is visible and can be removed once fixed. In short: validate strictly, change nothing implicitly, and document any necessary deviation from expected protocol behavior.

Example:
```python
# Validate against the RFC grammar before calling int()
# RFC 9112: Content-Length = 1*DIGIT and chunk-size = 1*HEXDIG.
# int() is more permissive, so we match against the grammar before calling it.
if not _content_length_re.fullmatch(value):
    raise ValueError("Invalid Content-Length")
length = int(value)
```