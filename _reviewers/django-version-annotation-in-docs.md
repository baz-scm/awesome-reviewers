---
title: Version annotation in docs
description: Always include appropriate version annotations when documenting new features
  or changes in behavior. Use `.. versionadded::` for new features and `.. versionchanged::`
  for modifications to existing functionality. Place these annotations immediately
  after the feature's first mention in the documentation.
repository: django/django
label: Documentation
language: Txt
comments_count: 5
repository_stars: 84182
---

Always include appropriate version annotations when documenting new features or changes in behavior. Use `.. versionadded::` for new features and `.. versionchanged::` for modifications to existing functionality. Place these annotations immediately after the feature's first mention in the documentation.

Example:
```rst
.. class:: NewFeature

    A new feature added to Django.

    .. versionadded:: 6.0

.. class:: ExistingFeature

    An existing feature with modified behavior.

    .. versionchanged:: 6.0
        Added support for new parameter and changed default behavior.
```

Key guidelines:
- Add version annotations for all new features, methods, classes, and settings
- Use versionchanged for behavioral changes, new parameters, or deprecations
- Place annotations before any detailed description or examples
- Include brief description of changes with versionchanged
- Target the next major version for changes in development

This helps users understand when features were introduced or modified, making documentation more maintainable and useful for different Django versions.