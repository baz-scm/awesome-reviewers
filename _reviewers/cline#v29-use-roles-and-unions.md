---
title: Use roles and unions
description: 'When implementing behavior that varies by mode/state (output format,
  session lifecycle, hook/tool context, etc.), avoid duplicated branching and near-identical
  helpers. Prefer:'
repository: cline/cline#v29
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 70893
---

When implementing behavior that varies by mode/state (output format, session lifecycle, hook/tool context, etc.), avoid duplicated branching and near-identical helpers. Prefer:

1) Role/factory objects over repeated `if/else` conditionals
- Create the appropriate “outputter”/handler once, then call a straight-line lifecycle API.

2) Discriminated unions over booleans for state
- Model multiple states explicitly (e.g., `resumed: "true" | "false" | "unknown"`-style unions) to prevent invalid combinations and make the code easier to test.

3) Single formatter/escaper for related variants
- If two functions only differ by a couple of attributes (tool identity vs run-start), unify them into one formatter that takes a discriminated union and applies escaping/wrapping rules in one place.

4) Reuse existing shared utilities
- If a check/transform already exists in a shared package, use it instead of adding local duplicates.

Example pattern (factory + discriminated union):

```ts
type RunContext =
	| { kind: "tool"; toolName: string; toolCallId: string; source: string; body: string }
	| { kind: "runStart"; source: string; body: string };

function formatHookContext(ctx: RunContext): string {
	const escaped = ctx.body.trim().replace(/<(\/?)hook_context/gi, "<\\$1hook_context");
	if (ctx.kind === "tool") {
		return `<hook_context source="${ctx.source}" tool_name="${ctx.toolName}" tool_call_id="${ctx.toolCallId}">\n${escaped}\n</hook_context>`;
	}
	return `<hook_context source="RunStart">\n${escaped}\n</hook_context>`;
}

// Choose once at startup
const outputter = config.outputMode === "json" ? new JsonRunOutputter() : new ConsoleRunOutputter();
outputter.runStarted({ verbose: config.verbose });
```

Use this checklist in code reviews:
- Are `if (mode === ...)` branches threaded throughout the function body? Prefer a single factory-created handler.
- Are booleans used to represent more than two meaningful states? Prefer a string/enum union.
- Are there two formatter functions that duplicate trimming/escaping/wrapping? Consolidate into one discriminated formatter.
- Is there a local helper that replicates something available in a shared module? Remove it and reuse the shared implementation.