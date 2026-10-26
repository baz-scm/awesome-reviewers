---
title: Maintain API Contract
description: 'Preserve external interface contracts so clients/consumers interpret
  inputs and wire formats consistently.


  Apply two core checks:

  1) Unambiguous parameter routing (CLI/API-style commands)'
repository: cline/cline#v23
label: API
language: Other
comments_count: 2
repository_stars: 70889
---

Preserve external interface contracts so clients/consumers interpret inputs and wire formats consistently.

Apply two core checks:
1) Unambiguous parameter routing (CLI/API-style commands)
- If a command forwards/dispatches arguments after a specific token (e.g., a “channel”/resource identifier), ensure option flags meant for the outer command appear before that token, and document the parsing/forwarding behavior.
- Example:
  - Prefer: `cline connect --restart telegram -k <BOT-TOKEN>`
  - Avoid: `cline connect telegram --restart -k <BOT-TOKEN>` (flag may be forwarded to the connector layer instead of the dispatcher)

2) Backward-compatible schema evolution (Protobuf/typed APIs)
- When removing enum values, do not reuse their numeric tags. Reserve both the number and name (or otherwise explicitly prevent reuse) to keep older clients from misinterpreting data.
- Example:
  - Instead of deleting an enum value outright, add:
    ```proto
    enum ClineAsk {
      // ...
      reserved 14;
      reserved "REPORT_BUG";
      // ...
    }
    ```

This prevents subtle “works locally” failures where consumers disagree on how inputs are parsed or what a numeric value means.