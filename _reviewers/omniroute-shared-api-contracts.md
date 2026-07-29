---
title: Shared API Contracts
description: 'Design API endpoints so they orchestrate transport only, and keep domain
  logic + contract identifiers centralized.


  Apply these rules:

  1) **Don’t couple libraries to route handlers**: HTTP-specific code (request/response/headers/params)
  stays in `route.ts`; core behavior (embeddings, memory indexing, etc.) lives in
  shared services used by both the API route...'
repository: diegosouzapw/OmniRoute
label: API
language: TSX
comments_count: 2
repository_stars: 33162
---

Design API endpoints so they orchestrate transport only, and keep domain logic + contract identifiers centralized.

Apply these rules:
1) **Don’t couple libraries to route handlers**: HTTP-specific code (request/response/headers/params) stays in `route.ts`; core behavior (embeddings, memory indexing, etc.) lives in shared services used by both the API route and other server modules.
2) **Single source of truth for backend-recognized identifiers**: any client/UI option that toggles engine behavior (rule names, modes, etc.) must use backend canonical constants/types—never “fabricated” strings.

Example pattern (service extraction):
```ts
// src/lib/embeddings/service.ts
export async function generateEmbeddings(input: string) {
  // domain logic here (no fetch/Response/route concerns)
}

// src/app/api/v1/embeddings/route.ts
import { generateEmbeddings } from "@/lib/embeddings/service";

export async function POST(req: Request) {
  const { input } = await req.json();
  const embeddings = await generateEmbeddings(input);
  return Response.json({ embeddings });
}
```

Example pattern (contract identifiers):
```ts
// shared/shared-rules.ts (or import from backend constant module)
export const ALL_CAVEMAN_RULES = [
  /* values copied/imported from backend canonical list */
] as const;

// UI uses the canonical list (no guessed strings)
import { ALL_CAVEMAN_RULES } from "@/shared/shared-rules";
```

If an option fails to work (e.g., skip/toggle doesn’t take effect), treat it as an API contract mismatch and trace the identifier back to its backend source of truth.