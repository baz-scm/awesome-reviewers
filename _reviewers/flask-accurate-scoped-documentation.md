---
title: Accurate, scoped documentation
description: Documentation—including changelogs, guides, tutorials, and inline examples—should
  be technically accurate, appropriately scoped, and free of misleading or unsafe
  guidance. Before writing a doc entry, verify the described behavior against the
  actual code (e.g., confirm blueprint template-loading order, or describe `sqlite3.Row`
  precisely as supporting both...
repository: pallets/flask
label: Documentation
language: Other
comments_count: 14
repository_stars: 75022
---

Documentation—including changelogs, guides, tutorials, and inline examples—should be technically accurate, appropriately scoped, and free of misleading or unsafe guidance. Before writing a doc entry, verify the described behavior against the actual code (e.g., confirm blueprint template-loading order, or describe `sqlite3.Row` precisely as supporting both tuple- and dict-like access rather than vaguely calling it "like a tuple"). Use correct markup (e.g., `:py:meth:` instead of plain text) so references render properly.

Keep each doc focused on its audience and purpose:
- Changelog entries belong only to user-facing, installable library changes; skip entries for internal docs/tooling updates, and follow the existing linking/format conventions (e.g., `:issue:`4054``) concisely, without restating implementation detail that isn't relevant to users.
- Narrative guides (quickstart, tutorials) should stay minimal and link to full API/reference docs for exhaustive details instead of duplicating them inline, e.g., don't reproduce the entire converter table in quickstart—summarize briefly and link to the API reference.

Code examples must be minimal and idiomatic for the context:
```python
# Bad: unused import, outdated syntax
from flask import Flask, request
print 'Initialized the database.'

# Good: only what's used, idiomatic for the context
from flask import request
click.echo('Initialized the database.')
```

Finally, avoid examples or callouts that nudge users toward insecure or discouraged practices (e.g., don't highlight `--host 0.0.0.0` for the dev server, and avoid naming/endorsing specific third-party tools unless necessary—prefer neutral language like "you may choose a different setup"). When in doubt about wording, favor precise, unambiguous phrasing over implying guarantees or side effects (e.g., clarify that template name collisions are resolved by registration order, not an error).</description>
</invoke>
