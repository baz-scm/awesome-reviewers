---
title: Public API Contract Completeness
description: When adding or extending an API/CLI surface that routes to backend providers,
  ensure the *public contract* is fully implemented end-to-end and that the payloads
  you generate for downstream systems are deterministic.
repository: openai/codex-security
label: API
language: TypeScript
comments_count: 2
repository_stars: 9394
---

When adding or extending an API/CLI surface that routes to backend providers, ensure the *public contract* is fully implemented end-to-end and that the payloads you generate for downstream systems are deterministic.

Apply these rules:
1) **No undocumented workarounds for supported features**: Every documented option must be accepted by validation, appear in schema/help, and map to the correct internal implementation.
   - Test the **real public path** (e.g., `--provider ...`) rather than hidden/raw flags.
2) **Deterministic structured serialization**: If you build request/prompt payloads from inputs that may contain commas/newlines/etc., serialize structured values as JSON (arrays/objects) instead of joining with delimiters or embedding raw text.
3) **Security assertions in provider-backed flows**: Authentication tests should verify required behavior while confirming credentials/tokens are not exposed in logs/output.

Example (provider option routing + deterministic payload formatting):
```ts
// 1) Public API contract: validate and route providers
const supportedProviders = new Set(["openai", "openrouter", "fireworks", "amazon-bedrock"]);
if (!supportedProviders.has(provider)) throw new Error("Unsupported provider");

const providerImpl = provider === "amazon-bedrock"
  ? builtInBedrockProvider
  : externalProviderRegistry[provider];

// 2) Deterministic structured serialization for downstream payload/prompt
const scopedPaths = ["a,b.txt", "c\n d.txt"]; // edge cases
const payload = {
  scopedPaths, // later serialized with JSON.stringify
};
const promptSection = `Scoped paths: ${JSON.stringify(payload.scopedPaths)}`;

// 3) Security test expectation (conceptual)
expect(stdout).not.toMatch(/AWS_(ACCESS_KEY_ID|SECRET_ACCESS_KEY)/);
```
