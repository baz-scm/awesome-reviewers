---
title: API contract verification
description: When updating any public interface (API schema, CLI flags/options, request
  parameters, or docs examples), verify the contract against the source of truth and
  the actual parser.
repository: cline/cline#v13
label: API
language: Other
comments_count: 2
repository_stars: 70874
---

When updating any public interface (API schema, CLI flags/options, request parameters, or docs examples), verify the contract against the source of truth and the actual parser.

Apply:
1) Regenerate schema/artifacts from the canonical definition instead of hand-editing generated files; then run the project’s generation/type-check commands.
2) Ensure docs and examples reflect real argument parsing: flags/options must appear in the position the parser expects (and in the order shown in the reference), otherwise the command may treat flags as connector/channel arguments.

Example (schema regeneration):
```sh
node scripts/generate-state-proto.mjs
npm run protos
npm run check-types
```

Example (CLI option ordering):
```md
# Correct: options before the connector/channel
cline connect telegram --restart -k <BOT-TOKEN>

# Avoid: putting CLI flags after the channel if the parser routes tail args to the connector
# cline connect telegram --restart -k <BOT-TOKEN>   (wrong in cases where tail args are forwarded)
```

Goal: keep user-facing interface behavior, documentation, and generated API/schema outputs consistent so changes don’t silently drift from what clients/devs actually experience.