---
title: Clear relationship descriptions
description: When documenting algorithms or data structures with graph-like relationships,
  use precise terminology to describe connections between elements. This is especially
  important when explaining how operations traverse or transform structured data.
repository: opentofu/opentofu
label: Algorithms
language: Markdown
comments_count: 2
repository_stars: 25901
---

When documenting algorithms or data structures with graph-like relationships, use precise terminology to describe connections between elements. This is especially important when explaining how operations traverse or transform structured data.

Distinguish explicitly between direct relationships and hierarchical ones to avoid implementation ambiguity. For example:

Instead of:
```
Remove vertices that are in (or children of items in) t.Excludes
```

Prefer:
```
Remove vertices that are in t.Excludes, or descendants of items in t.Excludes
```

Similarly, when describing behavioral relationships between components, use precise comparative language:

Instead of:
```
Method A should behave similarly with Method B
```

Prefer:
```
Method A should behave similarly to Method B
```

This precision prevents misinterpretation when implementing complex algorithms and makes relationships between components immediately clear to all readers, which is crucial when working with graph transformations, dependency trees, or other hierarchical data structures.