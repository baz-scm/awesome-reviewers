---
title: HTTP response construction
description: Use appropriate HTTP response construction methods and status codes for
  API endpoints. Prefer `Response.json()` over manual JSON stringification, return
  appropriate status codes (like 404 for unmatched routes), and avoid unnecessary
  response complexity when simple status codes suffice.
repository: cloudflare/workers-sdk
label: API
language: TypeScript
comments_count: 3
repository_stars: 3379
---

Use appropriate HTTP response construction methods and status codes for API endpoints. Prefer `Response.json()` over manual JSON stringification, return appropriate status codes (like 404 for unmatched routes), and avoid unnecessary response complexity when simple status codes suffice.

**Key practices:**
- Use `Response.json(data)` instead of `new Response(JSON.stringify(data), { headers: { "Content-Type": "application/json" } })`
- Return appropriate HTTP status codes (404 for not found, 2xx for success)
- Consider whether detailed response bodies are actually needed - some clients only care about status codes

**Example:**
```typescript
// ❌ Avoid manual JSON construction
return new Response(JSON.stringify({ success: true }), {
  status: 200,
  headers: { "Content-Type": "application/json" }
});

// ✅ Use Response.json() for JSON responses
return Response.json({ success: true });

// ✅ Return appropriate status codes for unmatched routes
if (!matchedRoute) {
  return new Response(null, { status: 404 });
}

// ✅ Simple responses when only status matters (e.g., webhooks)
return new Response("", { status: 200 });
```