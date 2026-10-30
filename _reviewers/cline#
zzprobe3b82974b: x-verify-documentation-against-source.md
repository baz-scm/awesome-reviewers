---
title: Verify documentation against source
description: 'Every factual claim in documentation — default values, file paths, option
  behavior, feature availability — must be verified against the actual current source
  code or observed runtime behavior before it is published, not assumed or carried
  over from memory. Several docs issues came from exactly this gap: a CLI help table
  said `--retries` defaults to 6 when...'
repository: 'cline/cline#

  zzprobe3b82974b: x'
label: Documentation
language: Other
comments_count: 6
repository_stars: 71067
---

Every factual claim in documentation — default values, file paths, option behavior, feature availability — must be verified against the actual current source code or observed runtime behavior before it is published, not assumed or carried over from memory. Several docs issues came from exactly this gap: a CLI help table said `--retries` defaults to 6 when `main.ts` actually applies `args.retries ?? 3`; a troubleshooting guide pointed to the wrong log file path because the author hadn't confirmed which process actually writes it (verified later via `lsof` and reading the writer's source); and a settings key was documented generically without checking that `gen-manifest.mjs` derives a different prefix for the nightly build, which would have silently broken for those users.

Apply this standard as follows:
- Before documenting a default, path, or behavior, check it against the relevant source file (e.g., argument parsing, manifest generation, log writer) rather than inferring it from adjacent code or prior docs.
- If a described behavior depends on an in-flight or unmerged change (e.g., a wizard that doesn't yet preserve a header value), do not document it as current behavior — either describe the actual current behavior and link to the pending PR, or hold the doc update until the change lands.
- If an option is accepted by the CLI but silently ignored, don't document it as if it works; omit it or explicitly note it's a no-op to avoid inviting misuse.
- When a feature is deprecated and no longer functionally effective (e.g., an ignore mechanism that can trivially be bypassed), prefer removing the documentation entirely over leaving a partial or caveated description that implies it still works.
- When describing behavior that varies across environments or providers (e.g., which model providers handle tool calls internally), give concrete, verifiable detail or an exhaustive/explained rule rather than a vague example that leaves users unable to determine which case applies to them.

The goal is that every statement in the docs can be traced to a verified source-of-truth, so readers never have to debug a problem caused by trusting inaccurate documentation.</description>
</invoke>
