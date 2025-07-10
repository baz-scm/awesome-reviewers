---
title: Consistent URL design
description: 'Design API endpoints with consistent, unambiguous URL patterns to improve
  usability and maintainability. Follow these principles:


  1. **Use descriptive parameter names** that clearly indicate their purpose'
repository: getsentry/sentry
label: API
language: Python
comments_count: 3
repository_stars: 41297
---

Design API endpoints with consistent, unambiguous URL patterns to improve usability and maintainability. Follow these principles:

1. **Use descriptive parameter names** that clearly indicate their purpose
   ```python
   # Bad: Generic parameter names
   r"^toolbar/(?P<project_id_or_slug>[^/]+)/(?P<project_id_or_slug>[^/]+)/"
   
   # Good: Specific parameter names that reflect their purpose
   r"^toolbar/(?P<organization_slug>[^/]+)/(?P<project_id_or_slug>[^/]+)/"
   ```

2. **Avoid path conflicts** between resource identifiers and action names
   When designing endpoints with both resource IDs and action names, choose naming conventions that avoid ambiguity. For example, use `-summary` suffix instead of nested paths:
   ```python
   # Potentially ambiguous: Is "summary" an ID or an action?
   r"^(?P<organization_id_or_slug>[^\/]+)/user-feedback/summary/$"
   
   # Better: Clearly distinguishes the summary action
   r"^(?P<organization_id_or_slug>[^\/]+)/feedback-summary/$"
   ```

3. **Support flexible parameter formats** for better client experience
   Design your parameter handling to support both multiple occurrences and array formats for list parameters:
   ```python
   # Support both formats:
   # - project=1&project=2  (multiple occurrences)
   # - project=[1,2]        (array format)
   
   # In URL documentation:
   ":qparam list[int] project: list of project IDs to filter by"
   
   # In implementation:
   project_ids = request.GET.getlist('project')
   ```

Consistent URL design makes your API more intuitive for clients to use and easier to maintain as it evolves.