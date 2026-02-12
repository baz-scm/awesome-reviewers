---
title: Specify API contracts
description: 'State and document explicit, unambiguous contracts for all API endpoints
  and RPC messages, especially around resource identity, data encoding, and file-operation
  semantics. Motivation: inconsistent assumptions about where a path comes from, whether
  payloads are encoded, and what ReadAt/WriteAt should return lead to brittle clients
  and surprising server...'
repository: wavetermdev/waveterm
label: API
language: Go
comments_count: 5
repository_stars: 17328
---

State and document explicit, unambiguous contracts for all API endpoints and RPC messages, especially around resource identity, data encoding, and file-operation semantics. Motivation: inconsistent assumptions about where a path comes from, whether payloads are encoded, and what ReadAt/WriteAt should return lead to brittle clients and surprising server behavior. How to apply:

- Resource identity in URLs: treat resources as RESTful paths when they represent server resources. Put file/config paths in the URL path segment rather than opaque query params so clients can request /config/keybindings.json or /files/{bucket}/{object}. Example: change

  // avoid reading resource from query
  qvals := r.URL.Query()
  filePath := qvals.Get("path")

  // prefer extracting from URL path (mux param or path prefix)
  // e.g. GET /config/{path}
  filePath := mux.Vars(r)["path"]

- Encoding contracts: document and enforce how binary data is transported. If a field is named data64, require base64 encoding at the producer side and decode at the consumer side. Make encoding explicit in code:

  // when producing file chunks
  chunk := buf[:n]
  resp.Data64 = base64.StdEncoding.EncodeToString(chunk)

  // when consuming
  data, err := base64.StdEncoding.DecodeString(resp.Data64)

- File operation semantics: define and document behavior for reads/writes with offsets. Choose one of these and be consistent:
  - Strict: return an error when WriteAt offset > file size (simple, predictable).
  - Sparse-supporting: allow writes past EOF by implicit zero-padding, but document performance implications and whether padding bytes count toward returned bytesWritten.

  If sparse writes are supported, prefer these rules: pad only as needed (e.g., block-level padding to avoid huge copies), do not include implicit padding bytes in the bytesWritten return value (return only the number of user bytes written), and ensure ReadAt returns zeros for any uninitialized region within the logical file range. Example contract: "WriteAt will left-pad up to MaxBlockSize in-memory for efficiency; returned bytesWritten excludes implicit zeros. ReadAt will return logical zeros for uninitialized regions within the file length."

- Responsibility boundaries: document which side normalizes/validates paths and who encodes/decodes payloads. For non-URL path formats acceptible to client libraries, document helper functions and keep server endpoints stable. Example: FileReadCommand should pass a well-formed FileData with Info.Path when the fileshare client is expected to own normalization:

  data, err := wshclient.FileReadCommand(RpcClient, wshrpc.FileData{Info: &wshrpc.FileInfo{Path: fmt.Sprintf(pattern, oid, fname)}}, ...)

- API surface ergonomics: prefer small, explicit signatures for public APIs. Use variadic parameters for option lists or alias checks (e.g., CheckOptionAlias(aliases ...string)) and avoid overusing generics where a simple interface suffices. Provide convenience helpers for common behaviors (e.g., SetInteractive(update, bool)).

Checklist for reviewers and implementers:
- Does the endpoint identify resources via path segments when appropriate? (discussion 0)
- Is there a documented encoding contract for binary fields (data64/base64)? Does code encode before setting and decode on receipt? (discussion 1)
- Are read/write offset semantics documented and consistent (error vs sparse write; returned byte counts)? (discussion 4)
- Are responsibilities for normalization and output modes clear between client and server? (discussions 2,3)
- Are API signatures simple and explicit; use variadic helpers when it improves clarity? (discussions 5,6)

Following these rules reduces surprises for clients, avoids implicit assumptions, and makes APIs easier to evolve and document.