---
title: Config Documentation Constraints
description: When adding or updating configuration-related docs (env vars, config
  files, feature/transport flags, and deployment commands), ensure the guidance is
  (1) context-correct, (2) compatibility-checked, and (3) explicit about defaults/overrides.
repository: infiniflow/ragflow
label: Configurations
language: Markdown
comments_count: 10
repository_stars: 80174
---

When adding or updating configuration-related docs (env vars, config files, feature/transport flags, and deployment commands), ensure the guidance is (1) context-correct, (2) compatibility-checked, and (3) explicit about defaults/overrides.

Apply this checklist:
- Context-match every file/command: clearly distinguish “source launch” vs “dockerized launch” and reference the correct config targets (e.g., templates vs generated configs; soft links vs real files).
- Declare incompatibilities and required flag combinations: if a mode requires disabling a transport/feature, state it as a hard rule with the exact flag.
- Make defaults explicit: explain what is enabled by default and how to disable/override specific behaviors with the corresponding “no-<flag>” options.
- Provide precision in examples: include the exact env var names, file paths, and command syntax; avoid ambiguous phrasing.
- Add a short “why” for non-obvious constraints (e.g., version pinning to keep entrypoint/image behavior consistent).

Example (flag compatibility + defaults):
```md
If you set `mcp-mode` to `host`, you must add `--no-transport-streamable-http-enabled`, because streamable-HTTP transport is not supported in host mode.
The legacy SSE transport and streamable-HTTP (JSON responses) are enabled by default unless explicitly disabled with the corresponding `--no-<flag>` options.
```

Example (context-correct config guidance):
- For source launch, instruct changes to the source config (e.g., `conf/service_conf.yaml`).
- For docker launch, instruct changes to the docker template (e.g., `docker/service_conf.yaml.template`), and don’t mix them in the same step.