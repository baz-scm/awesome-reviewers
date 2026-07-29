---
title: Contract-First API Validation
description: 'Treat every API endpoint as a contract:

  - Validate all request inputs (query params, body fields) with shared schemas (e.g.,
  Zod) instead of manual parsing.'
repository: diegosouzapw/OmniRoute
label: API
language: TypeScript
comments_count: 4
repository_stars: 33162
---

Treat every API endpoint as a contract:
- Validate all request inputs (query params, body fields) with shared schemas (e.g., Zod) instead of manual parsing.
- On validation failure, return a consistent 4xx (typically 400) rather than silently coercing/defaulting values.
- When transforming or wrapping responses (especially SSE/streaming), ensure the emitted wire format/shape matches what downstream clients parse.
- Normalize constructed upstream URLs/paths to avoid accidental double-appends/suffixes.

Example (pagination with schema validation):
```ts
export async function GET(request: Request) {
  const url = new URL(request.url);
  const offsetLimitRaw = {
    offset: url.searchParams.get("offset"),
    limit: url.searchParams.get("limit"),
  };

  // paginationSchema: offset int >= 0, limit int within an agreed range
  const validation = validateBody(paginationSchema, offsetLimitRaw);
  if (isValidationFailure(validation)) {
    return NextResponse.json({ error: validation.error }, { status: 400 });
  }

  const { offset, limit } = validation.data;
  const all = await getCombos();
  const combos = all.slice(offset, offset + limit);

  return NextResponse.json({ combos });
}
```

Team standard: no manual `parseInt`/fallback defaults for externally supplied API parameters; any transformation layer must preserve/emit the documented output shape.