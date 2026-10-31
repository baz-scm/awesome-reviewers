---
title: Document environment config scope
description: 'When documenting or introducing configuration mechanisms (env files,
  env vars, build/tox flags, config options), be explicit about what each mechanism
  is for, where it applies, and what is safe to commit to version control. Specifically:'
repository: pallets/flask
label: Configurations
language: Other
comments_count: 4
repository_stars: 75022
---

When documenting or introducing configuration mechanisms (env files, env vars, build/tox flags, config options), be explicit about what each mechanism is for, where it applies, and what is safe to commit to version control. Specifically:

- Never present secrets (API keys, passwords, credentials) and non-sensitive, shareable settings (like app entry points) as if they belong in the same file/mechanism. If an example shows a `.env` file, make clear whether it's meant to be committed or git-ignored, and warn that mixing secrets into a committed file is a common source of leaks.
- Clearly state the scope of a configuration mechanism: e.g., `.env` files are only loaded by `flask run`/`flask shell` via the CLI, not in production WSGI servers like gunicorn — so don't imply it solves production configuration too. Prefer scoped, environment-aware defaults (e.g., a committed `wsgi.py` entry point) over relying on uncommitted files for values needed in both dev and prod.
- Keep configuration examples and documented types/options accurate and specific to the tool/version in question (e.g., `tag_svn_revision` only works with SVN — use `tag_build`/`tag_date` for generic dev builds; don't widen a documented config type like `PERMANENT_SESSION_LIFETIME` to `float` just because it happens to work — document the intended, supported type).
- When adding environment-conditional settings (e.g., tox dependency markers), verify that default/common workflows (like `tox -e py`) still work unmodified, and document any special syntax (such as negation markers) since such conventions are often poorly documented elsewhere.

Example of a safer pattern instead of relying solely on `.env` for app location:
```python
# wsgi.py (safe to commit)
from myapp import create_app
application = create_app()
```
This avoids encouraging users to store `FLASK_APP`/secrets together in an uncommitted file while still giving a simple, committed entry point for both dev and production.</description>
</invoke>
