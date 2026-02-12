---
title: Prefer streaming operations
description: 'Motivation: avoid large, unnecessary memory allocations and excessive
  decoding or retention of full data sets. For parsing, logs, or history, operate
  on raw bytes or streams and read only the portion you need. For long-lived state,
  avoid keeping full large objects in memory—cap, page, or store lightweight references.'
repository: wavetermdev/waveterm
label: Performance Optimization
language: TypeScript
comments_count: 3
repository_stars: 17328
---

Motivation: avoid large, unnecessary memory allocations and excessive decoding or retention of full data sets. For parsing, logs, or history, operate on raw bytes or streams and read only the portion you need. For long-lived state, avoid keeping full large objects in memory—cap, page, or store lightweight references.

How to apply:
- Parse bytes, not decoded strings: work with Uint8Array slices and byte indexes so you only allocate what's needed and delay TextDecoder until you must produce text.
  Example (from change in discussion):
  let curLineBytes = new Uint8Array(this.rawData.buffer, this.parsePos, i - this.parsePos);
  let jsonStartIndex = curLineBytes.indexOf("{".charCodeAt(0));
  let byteSize = curLineBytes.slice(jsonStartIndex, curLineBytes.length).length;
  // only decode when needed: new TextDecoder().decode(curLineBytes.slice(jsonStartIndex))

- For large files (logs), do not read the entire file into memory. Use streaming APIs, read-from-end buffered seeks, or delegate to existing OS tools such as `tail -n` and capture output. If implementing in-process, read the file in chunks from the end until you have enough lines rather than reading the whole file.

- Manage in-memory history/state: avoid unbounded retention of large generated content. Options include capping history size, storing compact metadata or references, lazy-loading full content, or persisting to disk/DB and fetching on demand.

Why this improves performance: reduces peak memory usage, lowers GC pressure, and often speeds up operations by avoiding expensive encodings and unnecessary data copies. Follow this rule when designing parsers, log readers, and history/state storage to prevent scalability bottlenecks.