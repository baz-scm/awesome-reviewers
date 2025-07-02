---
title: Use CSS classes properly
description: Avoid inline styles and `!important` declarations in your HTML templates.
  Instead, define and use CSS classes that encapsulate styling needs. This improves
  code maintainability, readability, and reduces CSS specificity issues.
repository: kubeflow/kubeflow
label: Code Style
language: Html
comments_count: 2
repository_stars: 15064
---

Avoid inline styles and `!important` declarations in your HTML templates. Instead, define and use CSS classes that encapsulate styling needs. This improves code maintainability, readability, and reduces CSS specificity issues.

Bad example:
```html
<mat-icon style="height:72px !important; width:200px !important;" svgIcon="jupyterlab"></mat-icon>
```

Good example:
```html
<!-- In your HTML -->
<mat-icon class="server-type" svgIcon="jupyterlab"></mat-icon>

<!-- In your CSS -->
.server-type {
  height: 32px;
  width: 150px;
}

.server-type-wrapper {
  margin-bottom: 1rem;
}
```

This approach makes your styles more maintainable, easier to debug, and allows for better responsiveness. CSS classes can be reused across components and modified centrally rather than hunting through templates for inline styles.


[
  {
    "discussion_id": "595474491",
    "pr_number": 5646,
    "pr_file": "components/crud-web-apps/jupyter/frontend/src/app/pages/form/form-default/form-image/form-image.component.html",
    "created_at": "2021-03-16T19:20:17+00:00",
    "commented_code": "ML packages\"\n  icon=\"fa:fab:docker\"\n>\n  <section>\n    <div class=\"server-type\">Choose server type:</div>\n    <mat-button-toggle-group [formControl]=\"parentForm.get('serverType')\" aria-label=\"Server Type\">\n      <mat-button-toggle value=\"jupyter\" aria-label=\"Use JupyterLab based server\">\n        <mat-icon style=\"height:72px !important; width:200px !important;\" svgIcon=\"jupyterlab\"></mat-icon>",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "595474491",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5646,
        "pr_file": "components/crud-web-apps/jupyter/frontend/src/app/pages/form/form-default/form-image/form-image.component.html",
        "discussion_id": "595474491",
        "commented_code": "@@ -4,8 +4,23 @@\n   ML packages\"\n   icon=\"fa:fab:docker\"\n >\n+  <section>\n+    <div class=\"server-type\">Choose server type:</div>\n+    <mat-button-toggle-group [formControl]=\"parentForm.get('serverType')\" aria-label=\"Server Type\">\n+      <mat-button-toggle value=\"jupyter\" aria-label=\"Use JupyterLab based server\">\n+        <mat-icon style=\"height:72px !important; width:200px !important;\" svgIcon=\"jupyterlab\"></mat-icon>",
        "comment_created_at": "2021-03-16T19:20:17+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "Don't modify html elements directly with styles, always use a class instead that wraps what the style changes are. Also try to avoid as much as possible `!important` in CSS. Instead try to use more specific css selectors.\r\n\r\nHere you could introduce and use the following CSS class for each `<mav-icon>`\r\n```css\r\n.server-type {\r\n  height: 32px;\r\n  width: 150px;\r\n}\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "595475080",
    "pr_number": 5646,
    "pr_file": "components/crud-web-apps/jupyter/frontend/src/app/pages/form/form-default/form-image/form-image.component.html",
    "created_at": "2021-03-16T19:21:12+00:00",
    "commented_code": "ML packages\"\n  icon=\"fa:fab:docker\"\n>\n  <section>\n    <div class=\"server-type\">Choose server type:</div>\n    <mat-button-toggle-group [formControl]=\"parentForm.get('serverType')\" aria-label=\"Server Type\">",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "595475080",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5646,
        "pr_file": "components/crud-web-apps/jupyter/frontend/src/app/pages/form/form-default/form-image/form-image.component.html",
        "discussion_id": "595475080",
        "commented_code": "@@ -4,8 +4,23 @@\n   ML packages\"\n   icon=\"fa:fab:docker\"\n >\n+  <section>\n+    <div class=\"server-type\">Choose server type:</div>\n+    <mat-button-toggle-group [formControl]=\"parentForm.get('serverType')\" aria-label=\"Server Type\">",
        "comment_created_at": "2021-03-16T19:21:12+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "Add a wrapper class here to give this group a bottom margin\r\n\r\n```css\r\n.server-type-wrapper {\r\n  margin-bottom: 1rem;\r\n}",
        "pr_file_module": null
      }
    ]
  }
]
