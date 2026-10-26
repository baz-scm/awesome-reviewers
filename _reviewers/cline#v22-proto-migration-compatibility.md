---
title: Proto Migration Compatibility
description: When migrating Protobuf schemas, ensure (1) changes come from the correct
  source of truth via generators and are validated, and (2) removed enum values are
  explicitly reserved to prevent accidental reuse and maintain backward compatibility.
repository: cline/cline#v22
label: Migrations
language: Other
comments_count: 2
repository_stars: 70886
---

When migrating Protobuf schemas, ensure (1) changes come from the correct source of truth via generators and are validated, and (2) removed enum values are explicitly reserved to prevent accidental reuse and maintain backward compatibility.

- Generate/validate instead of hand-editing generated fields: re-run your proto generation pipeline from the authoritative inputs, then run the project’s proto/type checks to confirm the resulting schema matches expectations.
  ```sh
  node scripts/generate-state-proto.mjs
  npm run protos
  npm run check-types
  ```
- For enum migrations: if an enum entry is removed, reserve both its numeric value and (if used) its name so the value can’t be reintroduced later.
  ```proto
  enum SomeEnum {
    // ... existing values ...
    reserved 14;
    reserved "REPORT_BUG";
  }
  ```

Apply this anytime you change `.proto` files (especially generated ones) to keep migrations consistent, verifiable, and compatible across versions.