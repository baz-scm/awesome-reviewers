---
title: Configuration drift prevention
description: Prevent inconsistencies between configuration sources of truth (build
  config, extension manifests, and package metadata) that cause IDE/runtime surprises.
repository: QwenLM/qwen-code
label: Configurations
language: Json
comments_count: 4
repository_stars: 26407
---

Prevent inconsistencies between configuration sources of truth (build config, extension manifests, and package metadata) that cause IDE/runtime surprises.

Apply these rules when adding/updating any package/extension:

1) Mirror required build configuration options across comparable packages
- If the repo’s baseline/per-package convention includes a compiler option (e.g., declaration maps), add it to every similar production package that builds types.

Example (tsconfig.json):
```json
{
  "extends": "../../../tsconfig.json",
  "compilerOptions": {
    "declarationMap": true,
    "outDir": "dist",
    "rootDir": "src"
  }
}
```

2) Make manifest tool exposure explicit
- In MCP/extension manifests, pin which tools are included (e.g., `includeTools`) so trial/managed paths can’t accidentally expose more than intended later.

3) Declare or clearly document required env/config
- If a server requires env vars to start (e.g., `QWEN_EXTERNAL_CONTEXT_CONFIG`), surface that requirement in the extension manifest and/or the trial instructions so failures are actionable.

4) Keep version sources in sync
- When you bump workspace package versions, ensure `package-lock.json` and the workspace `package.json` versions agree (either bump the package.json or revert the lockfile entry) so the next `npm install` doesn’t silently rewrite lock state.

Net effect: consistent IDE navigation, predictable runtime behavior, and fewer “it works on my machine”/dirty lockfile/version drift issues.