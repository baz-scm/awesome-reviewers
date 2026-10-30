---
title: Bound network request risk
description: Every network call must enforce its own explicit bounds and preserve
  expected routing behavior — do not rely on cooperative server headers, global defaults,
  or only the "main" code path.
repository: 'cline/cline#

  zzprobe3b82974b: x'
label: Networking
language: TypeScript
comments_count: 4
repository_stars: 71067
---

Every network call must enforce its own explicit bounds and preserve expected routing behavior — do not rely on cooperative server headers, global defaults, or only the "main" code path.

1. Always attach a timeout or AbortSignal to outbound requests, including fallback/secondary paths. A fetch with no deadline can hang a user-facing flow indefinitely when a host drops packets instead of refusing the connection (slow/VPN-down/remote servers are far more common than a clean connection error). If a primary request is bounded, any fallback request triggered on its failure must be bounded too.

```ts
async function fetchModelIds(url: string, timeoutMs = 5000): Promise<string[]> {
	const response = await fetch(url, {
		signal: AbortSignal.timeout(timeoutMs),
	});
	return parseModelIds(await response.text());
}
```

2. Enforce size limits by counting bytes as they stream in, not by trusting a declared `Content-Length`. A missing or incorrect header must not allow unbounded buffering; cancel the read as soon as the running total exceeds the limit.

3. When introducing a proxy-aware dispatcher/agent, verify it preserves existing routing semantics such as loopback/`NO_PROXY` bypass. Libraries like undici's `EnvHttpProxyAgent` will proxy `127.0.0.1` traffic by default if `HTTP_PROXY` is set and `NO_PROXY` is absent, silently breaking local servers (e.g. Ollama/LM Studio) that previously worked. Add a regression test with the proxy env vars set and `NO_PROXY` unset to catch this.

4. Avoid unnecessary bulk network calls — fetch only what's needed for the current operation (e.g. a specific branch/ref) rather than pulling full remote state up front, especially before the user has confirmed an action.

Treat timeouts, size limits, and routing bypass rules as required, testable behavior for any new or modified network call, not optional hardening.</description>
