---
title: Config precedence and env overrides
description: When reading configuration from multiple sources (function arguments,
  environment variables, config files, defaults), implement and preserve a single,
  explicit precedence order, and ensure user-provided overrides beat environment-derived
  values.
repository: anthropics/anthropic-sdk-python
label: Configurations
language: Python
comments_count: 3
repository_stars: 3392
---

When reading configuration from multiple sources (function arguments, environment variables, config files, defaults), implement and preserve a single, explicit precedence order, and ensure user-provided overrides beat environment-derived values.

Apply this consistently:
- Define precedence clearly (example: “args > env vars > config > defaults”) and make the assignment/merge logic follow that order.
- When combining settings (e.g., proxy mounts/transports), merge so that explicit/user-provided values override environment-derived ones.
- Use syntax compatible with the project’s supported Python versions when merging/combining dicts (avoid newer operators if you must support older versions).
- In tests for env-driven behavior, assert stable, externally meaningful outcomes (e.g., correct mount presence/pattern), but avoid brittle checks that depend on internal transport behavior.

Example pattern (proxy mounts precedence):

```python
# env_proxies: dict[str, str|None]
proxy_map = {k: None if v is None else Proxy(url=v) for k, v in get_environment_proxies().items()}

proxy_mounts = {
    k: None if p is None else AsyncHTTPTransport(proxy=p, **transport_kwargs)
    for k, p in proxy_map.items()
}

# User mounts override env-derived mounts
mounts = dict(proxy_mounts)
mounts.update(kwargs.get("mounts", {}))
kwargs["mounts"] = mounts
```