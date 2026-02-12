---
title: Centralize database operations
description: 'Keep all SQL and DB-specific logic in a single dbops layer and expose
  a small, consistent API that handles common patterns: insert/update (use REPLACE/UPSERT),
  delete, queries, and serialization of complex fields. Motivation: reduces duplicated
  SQL across packages, avoids mismatch between INSERT vs UPDATE code paths, and centralizes...'
repository: wavetermdev/waveterm
label: Database
language: Go
comments_count: 2
repository_stars: 17328
---

Keep all SQL and DB-specific logic in a single dbops layer and expose a small, consistent API that handles common patterns: insert/update (use REPLACE/UPSERT), delete, queries, and serialization of complex fields. Motivation: reduces duplicated SQL across packages, avoids mismatch between INSERT vs UPDATE code paths, and centralizes serialization/transaction handling for sqlite or other stores.

How to apply (practical steps):
- Move DB functions (e.g., InsertFileIntoDB, WriteFileToDB, SetReleaseInfo) into a dbops package/file. Callers should pass typed objects; dbops performs SQL and serialization.
- Provide an upsert helper using REPLACE or an explicit UPSERT clause so you don't keep separate Insert vs Update functions:

Example (replace separate insert/update with REPLACE):
query := `REPLACE INTO block_file VALUES (?, ?, ?, ?, ?, ?, ?, ?)`
// tx.Exec(query, fileInfo.BlockId, fileInfo.Name, fileInfo.Opts.MaxSize, fileInfo.Opts.Circular, fileInfo.Size, fileInfo.CreatedTs, fileInfo.ModTs, metaJson)

- Centralize JSON serialization/deserialization: implement and reuse a small helper (quickJson/quickJSONEncode) for storing complex fields in sqlite to ensure consistent encoding and error handling. Example:

metaJson, err := quickJson(fileInfo.Meta)
if err != nil {
    return fmt.Errorf("error serializing meta for %s: %w", fileInfo.Name, err)
}
// then use metaJson in the REPLACE/UPSERT

- Keep transactions and error mapping in dbops: wrap DB operations with WithTx inside dbops so callers don't duplicate transaction boilerplate.

Checklist for changes:
- [ ] Create/extend dbops package and move DB functions there.
- [ ] Add Upsert/Replace helpers and use them for insert-or-update semantics.
- [ ] Add quickJson/quickJSONEncode and decode helpers; use them everywhere complex fields are stored.
- [ ] Update callers to use dbops API and remove in-package SQL code.

Benefit: clearer separation of concerns, fewer duplicated SQL code paths, consistent serialization, and easier maintenance and optimization of queries.