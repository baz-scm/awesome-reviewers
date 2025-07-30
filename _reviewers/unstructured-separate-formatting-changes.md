---
title: separate formatting changes
description: Keep formatting and style changes separate from functional code changes
  to maintain clear, reviewable diffs. When making functional changes, avoid simultaneously
  reordering imports, adjusting whitespace, or making other cosmetic modifications
  that obscure the actual logic changes. If formatting improvements are needed, submit
  them as standalone pull...
repository: Unstructured-IO/unstructured
label: Code Style
language: Other
comments_count: 2
repository_stars: 12117
---

Keep formatting and style changes separate from functional code changes to maintain clear, reviewable diffs. When making functional changes, avoid simultaneously reordering imports, adjusting whitespace, or making other cosmetic modifications that obscure the actual logic changes. If formatting improvements are needed, submit them as standalone pull requests.

This practice ensures that code reviewers can focus on the core logic changes without being distracted by formatting noise. It also makes it easier to track the history of functional changes and reduces the likelihood of merge conflicts.

Example of what to avoid:
```python
# Don't mix functional changes with formatting changes
@@ -1,19 +1,20 @@
 -c "constraints.in"
+backoff  # functional change
+# Also reordering other dependencies (formatting change)
```

Instead, submit formatting changes like dependency reordering as separate commits or pull requests. This keeps the diff focused on the actual functional change (adding the `backoff` dependency) rather than mixing it with unrelated organizational changes.