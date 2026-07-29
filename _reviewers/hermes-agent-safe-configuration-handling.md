---
title: Safe Configuration Handling
description: 'When configuration affects scripts (env vars, dotenv files, compatibility
  gates), treat it as serialized input/output and enforce correctness at three points:
  (1) safe encoding, (2) correct source scoping, and (3) declared bounds.'
repository: nousresearch/hermes-agent
label: Configurations
language: Shell
comments_count: 3
repository_stars: 221948
---

When configuration affects scripts (env vars, dotenv files, compatibility gates), treat it as serialized input/output and enforce correctness at three points: (1) safe encoding, (2) correct source scoping, and (3) declared bounds.

Apply this standard:
1) Escape/quote values you write into dotenv/shell syntax.
- If you emit `KEY="value"`, ensure the value has embedded `\` and `"` escaped so the generated line remains valid.
- Example pattern (shell):
  ```sh
  # value may contain backslashes and quotes; escape for a double-quoted dotenv token
  escaped="$value"
  escaped=$(printf '%s' "$escaped" | sed 's/\\/\\\\/g; s/"/\\"/g')
  echo "KEY=\"$escaped\""  # always double-quote the serialized token
  ```

2) Scope config-file reads to the explicit boundary variable.
- If the project defines `HERMES_ENV_FILE`, only read the token(s) from that file.
- Avoid accidental fallback to a different default profile when `HERMES_HOME` (or similar) is set.

3) Enforce compatibility ranges exactly as declared.
- If the project declares support (e.g., `requires-python`), bound your “>=” checks to that range; don’t assume a broader interpreter is usable.
- Add regression coverage for the upper bound rejection (e.g., reject 3.14 when support is `<3.14`).

Net effect: generated config remains parseable, scripts read the intended configuration source, and installations/feature gates behave consistently with the project’s declared support.