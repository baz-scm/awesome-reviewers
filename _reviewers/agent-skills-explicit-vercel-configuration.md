---
title: Explicit Vercel Configuration
description: 'Treat Vercel deployment as a configuration contract: declare dependency/version/runtime
  settings explicitly and align your code layout with Vercel’s discovery (or override
  it explicitly).'
repository: vercel-labs/agent-skills
label: Configurations
language: Markdown
comments_count: 5
repository_stars: 26385
---

Treat Vercel deployment as a configuration contract: declare dependency/version/runtime settings explicitly and align your code layout with Vercel’s discovery (or override it explicitly).

Apply this standard:

1) Pick the correct dependency manifest/lock strategy
- For new projects, use `pyproject.toml` as the primary manifest.
- Use the lockfile that matches it (`uv.lock` / `pylock.toml` for `pyproject.toml` projects). Don’t mix Pipfile lockfiles as “the” lock for `pyproject.toml` projects.

2) Declare supported Python versions
- Only target Vercel-supported versions (3.12/3.13/3.14 for new projects).
- If you need an exact minor runtime, set `.python-version` (e.g., `3.13`).
- If you need compatibility, set `project.requires-python` with a bounded range (e.g., `>=3.12,<3.15`).

3) Ensure entrypoint discovery always works
- Prefer conventional filenames and shallow directories (e.g., `app.py`, `main.py`, `asgi.py` in the root or `src/`, `app/`, `api/`).
- Export exactly one top-level callable that Vercel can find: `app`, `application`, or `handler`.
- If your layout is nonstandard, explicitly override with `[tool.vercel].entrypoint`.

4) Match framework “shape” to dependencies
- FastAPI (ASGI) must include an ASGI server dependency (commonly `uvicorn`); Flask (WSGI) should not rely on ASGI server wiring.

5) Don’t make discovery depend on missing local env/config
- If your settings/imports/symbols depend on environment variables or other config, ensure those values are defined in the Vercel project so the build/runtime environment can resolve them.

Example `pyproject.toml` wiring:
```toml
[project]
requires-python = ">=3.12,<3.15"

[tool.vercel]
entrypoint = "api/main.py"
```

If Vercel reports entrypoint/callable not found, fix it by updating (a) the entrypoint path override, (b) conventional filename/path placement, and (c) top-level callable exports—then ensure any required env/settings are configured in Vercel.