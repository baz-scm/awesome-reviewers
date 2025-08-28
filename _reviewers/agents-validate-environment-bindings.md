---
title: Validate environment bindings
description: Always validate that environment bindings exist and are of the expected
  type before using them, and ensure external dependencies are properly configured
  in build scripts. Runtime binding validation prevents cryptic errors when bindings
  are missing or misconfigured, while proper build configuration prevents dynamic
  import issues in serverless environments.
repository: cloudflare/agents
label: Configurations
language: TypeScript
comments_count: 2
repository_stars: 2312
---

Always validate that environment bindings exist and are of the expected type before using them, and ensure external dependencies are properly configured in build scripts. Runtime binding validation prevents cryptic errors when bindings are missing or misconfigured, while proper build configuration prevents dynamic import issues in serverless environments.

For runtime validation, check both existence and type:
```ts
const bindingValue = env[binding as keyof typeof env] as unknown;

// Ensure we have a binding of some sort
if (bindingValue == null || typeof bindingValue !== "object") {
  console.error(
    `Could not find binding for ${binding}. Did you update your wrangler configuration?`
  );
  return new Response("Invalid binding", { status: 500 });
}

// Ensure that the binding is to a DurableObject
if (bindingValue.toString() !== "[object DurableObjectNamespace]") {
  return new Response("Invalid binding", { status: 500 });
}
```

For build configuration, include external packages in your build scripts and use top-level imports instead of dynamic imports:
```ts
// In build.ts - add external packages
external: ["cloudflare:email", "other-external-packages"]

// In code - use top-level imports
import { createMimeMessage } from "mimetext";
import { EmailMessage } from "cloudflare:email";
```