---
title: Consistent, descriptive identifiers
description: Choose names that are specific, self-explanatory, and consistent with
  the rest of the codebase. Before introducing a new option, type, or generic parameter,
  search for existing analogous APIs and reuse their naming pattern instead of inventing
  a new one (e.g. use `headerName` because bearer-auth/JWT/JWK middleware already
  use it, instead of `header` or...
repository: HONOJS/HONO
label: Naming Conventions
language: TypeScript
comments_count: 22
repository_stars: 32741
---

Choose names that are specific, self-explanatory, and consistent with the rest of the codebase. Before introducing a new option, type, or generic parameter, search for existing analogous APIs and reuse their naming pattern instead of inventing a new one (e.g. use `headerName` because bearer-auth/JWT/JWK middleware already use it, instead of `header` or `authorization`; use generic `E` for an `Env` type parameter instead of `TEnv`; keep platform-specific exports like `toSSG` aligned across adapters). Avoid vague, overly generic, or ambiguous terms such as `strict`, `header`, `Config`, or `AfterHook` — prefer explicit alternatives like `alwaysRedirect`, `headerName`, `TimingOptions`, or `AfterResponseHook` that make the purpose obvious without reading the implementation or docs. When mirroring external specs or libraries (HTML attributes, DOM types), match their exact casing (e.g. `srcdoc`, not `srcDoc`; `disablePictureInPicture` kept camelCase) and when forming acronym-based names follow established JS conventions (`URL`, `URLSearchParams` style, e.g. `ToSSGResult` not `ToSsgResult`). For boolean-like or deprecated options, pick names that clearly state behavior rather than relying on ambiguous adjectives, and prefer a single clear option over introducing confusing `@deprecated` aliases. Finally, exported middleware/handler factories should return a **named** function expression matching the public function's name (e.g. `return async function ipRestriction(c, next) { ... }`) so the identifier is visible in stack traces and debugging tools, consistent with other core middleware.