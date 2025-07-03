---
title: Mark UI text i18n
description: All user-facing text in HTML templates should be marked for internationalization
  using the i18n directive. This includes labels, placeholders, error messages, and
  any other text displayed to users. Using the i18n directive ensures the text can
  be properly extracted for translation and maintains consistent internationalization
  throughout the application.
repository: kubeflow/kubeflow
label: Documentation
language: Html
comments_count: 3
repository_stars: 15064
---

All user-facing text in HTML templates should be marked for internationalization using the i18n directive. This includes labels, placeholders, error messages, and any other text displayed to users. Using the i18n directive ensures the text can be properly extracted for translation and maintains consistent internationalization throughout the application.

Example:
```html
<!-- Incorrect -->
<mat-label>{{ 'common.name' | translate }}</mat-label>
<input matInput placeholder="{{ 'common.name' | translate }}" [formControl]="nameControl" />

<!-- Correct -->
<mat-label i18n>Name</mat-label>
<input matInput placeholder="Name" i18n-placeholder [formControl]="nameControl" />
```

Note that for attributes like placeholders, use the i18n-attribute syntax (e.g., i18n-placeholder) to mark them for translation.
