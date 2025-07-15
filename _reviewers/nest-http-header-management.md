---
title: HTTP header management
description: 'When working with HTTP responses, follow these principles for proper
  header management:


  1. **Only set default headers when undefined, not when falsy:**'
repository: nestjs/nest
label: Networking
language: TypeScript
comments_count: 4
repository_stars: 71766
---

When working with HTTP responses, follow these principles for proper header management:

1. **Only set default headers when undefined, not when falsy:**
   ```typescript
   if (!response.getHeader('Content-Type')) {
     response.setHeader('Content-Type', 'application/octet-stream');
   }
   ```
   This preserves intentionally set falsy values while ensuring compatibility between different HTTP adapters like Express and Fastify.

2. **For specialized protocols like Server-Sent Events (SSE)**, include all necessary headers for proxy compatibility:
   ```typescript
   response.writeHead(200, {
     'Content-Type': 'text/event-stream; charset=utf-8',
     'Cache-Control': 'private, no-cache, no-store, must-revalidate, max-age=0, no-transform',
     'X-Accel-Buffering': 'no'
   });
   ```
   Avoid setting headers that should be determined by the server, such as `Transfer-Encoding`.

3. **For redirects**, use standard HTTP status codes with 302 (FOUND) as the default:
   ```typescript
   public redirect(response: any, statusCode: number, url: string) {
     const code = statusCode ? statusCode : HttpStatus.FOUND;
     // implementation
   }
   ```

4. **Maintain consistency** between different HTTP adapters to ensure predictable behavior across platforms.