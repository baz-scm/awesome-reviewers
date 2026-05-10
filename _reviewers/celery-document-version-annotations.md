---
title: Document version annotations
description: When a doc section introduces a new configuration option or feature,
  include accurate version metadata (Celery and, when relevant, the dependency/library
  version). Missing or incorrect `.. versionadded::` causes confusion about availability.
repository: celery/celery
label: Documentation
language: Other
comments_count: 10
repository_stars: 28464
---

When a doc section introduces a new configuration option or feature, include accurate version metadata (Celery and, when relevant, the dependency/library version). Missing or incorrect `.. versionadded::` causes confusion about availability.

Apply this when you add:
- a new `.. setting:: <name>` block
- a new behavior/feature in guides
- a change that depends on a specific Kombu (or other library) version

Template (reST):

```rst
.. setting:: my_new_setting

``my_new_setting``
~~~~~~~~~~~~~~~~~~

Default: <value>

.. versionadded:: 5.7

<one- to two-sentence description of what it does>
```

If the behavior depends on Kombu, specify the Kombu version in the same style (e.g., “.. versionadded:: Kombu 5.6.0”). Avoid adding redundant anchors when using Sphinx directives like `.. setting::` that already create anchors.