---
title: Translation layer fidelity
description: When building proxy/translation layers between different API or protocol
  formats (e.g., OpenAI-to-Claude streaming translation, built-in-tool fallback substitution),
  preserve the exact semantics of the original request/response and never silently
  alter client-specified behavior. Guard every state transition with explicit flags
  (e.g. `toolInfo.closed`,...
repository: Decolua/9Router
label: API
language: JavaScript
comments_count: 3
repository_stars: 31641
---

When building proxy/translation layers between different API or protocol formats (e.g., OpenAI-to-Claude streaming translation, built-in-tool fallback substitution), preserve the exact semantics of the original request/response and never silently alter client-specified behavior. Guard every state transition with explicit flags (e.g. `toolInfo.closed`, `finishReasonSent`, `messageStopSent`) so that protocol events (tool-block stops, finish reasons, message stops) are emitted exactly once even when multiple upstream signals arrive — duplicate or missing events corrupt the client's view of the stream. If a fallback/substitute implementation cannot fully honor a constraint the client requested (e.g., a search tool scoped to an internal index with `external_web_access:false`), disable the fallback entirely and pass the request through untouched rather than rerouting it through a provider that violates the requested scope. Keep the public surface of such translation functions minimal: don't add parameters (e.g., an `onProgress` callback) for features that aren't yet wired up, since unused options add confusion and future compatibility risk. Add regression tests that specifically cover these edge cases (late chunks carrying usage, scoped search requests) to lock in the correct behavior.