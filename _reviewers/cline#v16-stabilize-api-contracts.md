---
title: Stabilize API contracts
description: When defining or documenting an API/contract (including CLI-driven APIs
  and serialized wire formats), ensure both *input semantics* and *wire identifiers*
  remain stable and unambiguous.
repository: cline/cline#v16
label: API
language: Other
comments_count: 2
repository_stars: 70882
---

When defining or documenting an API/contract (including CLI-driven APIs and serialized wire formats), ensure both *input semantics* and *wire identifiers* remain stable and unambiguous.

- **Make flag/parameter routing deterministic:** If your command/API forwards “everything after X” to a downstream handler, place options before the positional/channel argument so they reach the intended layer.
  ```sh
  # Prefer: options before the channel/target
  cline connect telegram --restart -k <BOT-TOKEN>

  # Avoid: placing options after the channel if the implementation forwards them away
  # cline connect telegram --restart -k <BOT-TOKEN>
  # (only the portion before the forwarded boundary is interpreted by the top-level command)
  ```
- **Preserve serialized identifiers (protobuf, enums, codes):** Never reuse numeric values (or names) of removed/renamed enum entries; reserve them.
  ```proto
  enum ClineAsk {
    SUMMARIZE_TASK = 15;
    reserved 14;
    reserved "REPORT_BUG";
  }
  ```

Apply this by aligning docs/examples with actual parsing/forwarding logic, and by treating wire-format identifiers as immutable—changes should be additive, with explicit reservations/deprecations when removal is needed.