---
title: Timeout and proxy correctness
description: 'Network requests must have deliberate, consistent timeout and proxy
  behavior, not accidental defaults. Before adding or removing a client-side deadline,
  reason explicitly about what happens on each side: a request with no timeout should
  only be used when the server''s eventual response still matters (e.g. committing
  a slow-but-successful operation) and some...'
repository: 'cline/cline

  '
label: Networking
language: TypeScript
comments_count: 3
repository_stars: 70942
---

Network requests must have deliberate, consistent timeout and proxy behavior, not accidental defaults. Before adding or removing a client-side deadline, reason explicitly about what happens on each side: a request with no timeout should only be used when the server's eventual response still matters (e.g. committing a slow-but-successful operation) and some other layer bounds the user-visible wait; a request that can legitimately take a long time (e.g. waiting on a local/remote model's first token) should have idle/body timeouts disabled or extended rather than left at a generic default that kills it mid-stream. Apply the same care to every code path that can serve a request, including fallbacks — a primary call protected by an AbortSignal is not enough if a secondary `fetch` call in the same flow has no timeout at all, since that turns a fast failure into an indefinite hang.

When introducing a custom dispatcher/agent (for proxy support, custom timeouts, etc.), verify it preserves existing routing guarantees such as NO_PROXY/loopback bypass. Libraries like undici's `EnvHttpProxyAgent` will proxy `localhost`/`127.0.0.1` traffic whenever `HTTP_PROXY`/`HTTPS_PROXY` is set and `NO_PROXY` is absent, silently breaking local model servers (LM Studio, Ollama) that previously connected directly. Route loopback hosts through a plain, no-proxy agent and only send non-loopback hosts through the environment-proxy agent. Add regression tests that set the proxy env vars without `NO_PROXY` and assert loopback connects directly while a non-loopback host is proxied — tests that unset both vars do not exercise this behavior at all.