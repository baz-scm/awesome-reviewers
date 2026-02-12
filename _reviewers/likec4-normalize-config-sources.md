---
title: normalize config sources
description: 'Ensure all runtime and project configuration is explicit, type-safe,
  and machine-independent.


  Motivation

  - Implicit or ad-hoc config (raw process.env usage, feature flags only in local
  env, or file:///absolute asset paths) causes type errors, unresolved imports, and
  “works on my machine” failures in CI and collaborators’ environments.'
repository: likec4/likec4
label: Configurations
language: TypeScript
comments_count: 3
repository_stars: 2582
---

Ensure all runtime and project configuration is explicit, type-safe, and machine-independent.

Motivation
- Implicit or ad-hoc config (raw process.env usage, feature flags only in local env, or file:///absolute asset paths) causes type errors, unresolved imports, and “works on my machine” failures in CI and collaborators’ environments.

Rules (actionable)
1. Use a typed env accessor and parse values with defaults
   - Avoid raw process.env access across codebase. Use a shared helper (e.g. std-env or a thin wrapper) so values are typed and consistent.
   - Parse numeric/env values explicitly and provide sane defaults.
   Example:
   import { env } from 'std-env'

   const preferredPort = env.PORT ? parseInt(env.PORT, 10) : 5173

2. Put feature flags and experimental toggles in project config
   - Add an explicit experimental block to your project schema so flags are part of repository config and travel with the project/CI.
   - Prefer schema validation (Zod or equivalent) so configs are discoverable and validated at startup/build time.
   Example:
   export const LikeC4ExperimentalSchema = z.object({
     dynamicViewBranches: z.boolean().optional().meta({ description: '...' })
   })

   export const LikeC4ProjectJsonConfigSchema = z.object({
     // ...
     experimental: LikeC4ExperimentalSchema.optional()
   })

3. Normalize asset and file paths in generated/virtual modules
   - Disallow file:// URIs in model/config data. Convert them to repository-relative or project-root-relative paths.
   - When emitting imports in virtual modules for Vite, compute paths relative to the source file or use Vite’s filesystem prefix (/@fs) if appropriate. Test that ?inline requests resolve in dev and build.
   - Detect local images (e.g. startsWith('.') or no protocol) and rewrite imports so Vite can resolve them: e.g. `import Icon from './path/to/icon.svg?inline'` or `/@fs/path/to/icon.svg?inline` after computing correct project-relative path.

Checks to run
- Typecheck: ensure env access types and schema types pass.
- Dev server import-analysis: run Vite and verify no "Failed to resolve import" errors for generated virtual modules.
- CI reproducibility: ensure project config (including experimental flags) is present in repository and yields same behavior in CI as locally.

Why this helps
- Makes configuration explicit and versioned with the project (avoids "works on my machine").
- Prevents subtle runtime failures from unresolved imports or incorrect env parsing.
- Improves developer experience and CI reliability by standardizing where and how configuration is read and validated.