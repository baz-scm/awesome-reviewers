---
title: RFC-compliant protocol handling
description: 'When implementing HTTP-related features—header generation/parsing, charset
  declarations, content negotiation, or IP address comparisons—validate behavior against
  the governing RFC/IANA specification rather than relying on assumptions or ad-hoc
  string checks. Common pitfalls include: using an internal encoding alias (e.g. Node''s
  `utf8`) instead of the...'
repository: expressjs/Express
label: Networking
language: JavaScript
comments_count: 6
repository_stars: 69579
---

When implementing HTTP-related features—header generation/parsing, charset declarations, content negotiation, or IP address comparisons—validate behavior against the governing RFC/IANA specification rather than relying on assumptions or ad-hoc string checks. Common pitfalls include: using an internal encoding alias (e.g. Node's `utf8`) instead of the IANA-registered value (`utf-8`) in an HTTP header, which breaks interoperability even though Node accepts it internally; building header value grammars (e.g. Link header rel/attribute tokens) with regexes that don't match the RFC's token/extended-notation/quoted-string productions; naively treating `Accept: */*` as "accept everything" without considering ordering, quality values, or that this policy decision may belong at the application layer rather than being hardcoded in the framework; and comparing IP addresses as raw strings without normalizing representations (e.g. `FE80::1` vs `fe80::1`, or IPv4-mapped IPv6 addresses like `::ffff:127.0.0.1`), causing valid matches to be missed. Before merging protocol-handling code, cross-check edge cases against the relevant RFC and existing test suites, and prefer well-tested parsing/normalization utilities over custom string manipulation. For example, when setting an Accept/Content-Type charset:

```js
// Wrong: not a valid HTTP charset token
res.set('Content-Type', setCharset(type, 'utf8'));

// Correct: use the IANA-registered name
res.set('Content-Type', setCharset(type, 'utf-8'));
```

Document any deliberate deviation from spec behavior and add regression tests covering the RFC edge cases you considered.