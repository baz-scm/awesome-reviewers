---
title: API documentation clarity
description: Ensure API parameter documentation clearly specifies default values,
  valid options, error conditions, and precise requirements to prevent user confusion
  and integration failures. Ambiguous documentation leads to misunderstandings about
  expected behavior and can cause integration problems.
repository: argoproj/argo-cd
label: API
language: Markdown
comments_count: 3
repository_stars: 20149
---

Ensure API parameter documentation clearly specifies default values, valid options, error conditions, and precise requirements to prevent user confusion and integration failures. Ambiguous documentation leads to misunderstandings about expected behavior and can cause integration problems.

When documenting API parameters, always include:
- Explicit default values and their behavior
- Complete list of valid parameter values
- Clear distinction between "not providing the parameter" vs "providing empty value"
- Precise requirements for external integrations (like API scopes)

Example of improved documentation:
```
--filter-fields strings   A comma separated list of fields to display. If not specified, displays entire manifest. Valid values: field names separated by commas. (Optional)

pullRequestState: Additional filter for MRs by state. Default: "" (all states). Valid values: "", "opened", "closed", "merged", "locked" (Optional)

API scope: Must strictly include https://www.googleapis.com/auth/admin.directory.group.readonly. Using broader scopes like https://www.googleapis.com/auth/admin.directory.group will cause API failures.
```

This prevents user confusion about default behavior, error conditions, and integration requirements.