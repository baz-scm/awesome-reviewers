---
title: Config precedence consistency
description: For configuration-driven code (especially anything that affects user-facing
  URLs, published links, secrets, or server startup), centralize resolution and make
  precedence explicit.
repository: the-pr-agent/pr-agent
label: Configurations
language: Python
comments_count: 5
repository_stars: 12523
---

For configuration-driven code (especially anything that affects user-facing URLs, published links, secrets, or server startup), centralize resolution and make precedence explicit.

Apply these rules:
1) Use a single “resolver” per concept (e.g., user-facing base URL, webhook secret). All output paths must use it—no bypasses.
2) Define and document an explicit precedence order. Prefer dedicated user-facing settings over API/internal settings.
3) Handle “shipped defaults” safely: treat the default value as non-overriding (compare against a DEFAULT constant) so real deployments don’t regress.
4) Avoid duplicated fallback expressions for secrets/configs. Keep backwards compatibility in the resolver, not scattered across handlers.
5) Use consistent config access (`get_settings().get(...)`) and prefer config/env-backed values for ports.

Example (user-facing URL resolver pattern):
```python
DEFAULT_GITEA_URL = "https://gitea.com"

def resolve_user_facing_base(pr, owner, repo, pr_number, base_url: str) -> str:
    web_url = (get_settings().get("GITEA.WEB_URL", "") or "").rstrip("/")
    if web_url:
        return web_url

    configured = (get_settings().get("GITEA.URL", "") or "").rstrip("/")
    if configured and configured != DEFAULT_GITEA_URL:
        return configured

    pr_html_url = getattr(pr, "html_url", "") if pr else ""
    suffix = f"/{owner}/{repo}/pulls/{pr_number}"
    if pr_html_url and pr_html_url.endswith(suffix):
        return pr_html_url[: -len(suffix)]

    return base_url
```
Then ensure every user-facing link builder (comments, changelog links, review links) uses this resolved base, not the API/internal `base_url`.