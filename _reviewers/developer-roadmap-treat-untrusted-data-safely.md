---
title: Treat Untrusted Data Safely
description: 'Security rule: Treat anything from the client (sessions, form fields,
  query params, template-bound values) as untrusted at runtime. Enforce safety on
  the server and use framework safe defaults for output encoding/sanitization. Only
  use “bypass”/escape hatches when you can prove the value’s origin and safety, and
  document that proof.'
repository: kamranahmedse/developer-roadmap
label: Security
language: Markdown
comments_count: 4
repository_stars: 354523
---

Security rule: Treat anything from the client (sessions, form fields, query params, template-bound values) as untrusted at runtime. Enforce safety on the server and use framework safe defaults for output encoding/sanitization. Only use “bypass”/escape hatches when you can prove the value’s origin and safety, and document that proof.

How to apply
- Authentication/session handling: On every request that depends on a user session, validate the session identifier server-side; invalidate/destroy it on logout.
- Input validation: Do not rely on TypeScript types for client input safety. Validate at runtime with a schema validator (e.g., Zod) for forms, API contracts, and persisted data.
- Output safety (XSS): Use the framework’s default escaping/sanitization for template interpolation/bindings.
- Narrow trust exceptions: If you must disable sanitization (e.g., Angular’s DomSanitizer bypass*), only do it after you inspected how the value was created and verified it cannot contain attacker-controlled payloads. If you can’t prove that, don’t bypass.

Example patterns
- Runtime input validation (Zod):
```ts
import { z } from "zod";

const LoginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(1),
});

export function parseLogin(body: unknown) {
  return LoginSchema.parse(body); // runtime validation
}
```
- XSS-safe output (Angular):
  - Prefer normal template bindings/interpolation so Angular sanitizes/escapes by default.
- Risky bypass guarded by proof (Angular):
```ts
import { DomSanitizer } from "@angular/platform-browser";

export class ExampleComponent {
  trustedUrl: any;

  constructor(private sanitizer: DomSanitizer) {
    // Only bypass when you *proved* the value is not attacker-controlled
    // and you constructed it from trusted sources.
    const trusted = "https://example.com/safe-path";
    this.trustedUrl = this.sanitizer.bypassSecurityTrustUrl(trusted);
  }
}
```

Team checklist
- [ ] Server validates session IDs on protected endpoints
- [ ] All external inputs are validated at runtime with schemas
- [ ] UI output uses safe defaults (escaping/sanitization)
- [ ] Sanitization bypasses are prohibited unless a documented, verifiable safety check exists