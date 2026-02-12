---
title: defensive null handling
description: 'Always handle nullable values explicitly and defensively to prevent
  runtime null/undefined errors and to make intent clear.


  Why: Nulls and undefined values cause intermittent runtime exceptions and unclear
  state transitions. Being explicit—both when clearing values and when checking inputs—reduces
  bugs and documents intent.'
repository: wavetermdev/waveterm
label: Null Handling
language: TypeScript
comments_count: 2
repository_stars: 17328
---

Always handle nullable values explicitly and defensively to prevent runtime null/undefined errors and to make intent clear.

Why: Nulls and undefined values cause intermittent runtime exceptions and unclear state transitions. Being explicit—both when clearing values and when checking inputs—reduces bugs and documents intent.

Rules to follow:
- Use optional chaining or explicit null/undefined checks before accessing properties or collection lengths (e.g., workspaceList?.length).
- Wrap parsing/decoding in try/catch and set values to null when parsing fails or data is absent to represent a cleared value.
- When multiple related conditions control behavior, combine them so the intended branch is obvious and you don’t accidentally act on a null value.

Examples (based on discussion snippets):
1) Defensive parsing and explicit null to clear state

try {
    const decodedCmd = atob(cmd.data.cmd64);
    rtInfo["shell:lastcmd"] = decodedCmd;
} catch (e) {
    console.error("Error decoding cmd64:", e);
    // null used intentionally to clear the key
    rtInfo["shell:lastcmd"] = null;
}

2) Combine guards and use optional chaining for nullable collections

if (ww?.workspaceId === workspaceId) {
    if (workspaceList?.length > 1) {
        // switch workspace
    } else {
        // delete workspace
    }
}

Apply these consistently: prefer explicit null to indicate cleared/absent values, guard all external inputs and collections with optional chaining or null checks, and structure conditionals to make null-handling intent obvious.