---
title: Component-agnostic styling principles
description: Create reusable components with styles that don't make assumptions about
  parent contexts or affect their positioning in different applications. Keep positioning
  styles (like margins) in the parent components that use them rather than in the
  reusable component itself. Prefer properties that don't assume parent styling context.
repository: kubeflow/kubeflow
label: Code Style
language: Css
comments_count: 2
repository_stars: 15064
---

Create reusable components with styles that don't make assumptions about parent contexts or affect their positioning in different applications. Keep positioning styles (like margins) in the parent components that use them rather than in the reusable component itself. Prefer properties that don't assume parent styling context.

**Instead of this:**
```scss
// In a reusable component
.panel-body {
  margin-top: 5px;  // Affects positioning
  flex: 1;  // Assumes parent has display: flex
}
```

**Do this:**
```scss
// In a reusable component
.panel-body {
  padding: 1px;  // Internal spacing only
  height: 100%;  // Fills available space without assumptions
}

// In the parent component that uses it
.parent-container .panel-body {
  margin-top: 5px;  // Position-affecting styles belong here
}
```

This approach ensures components remain flexible and can be reused in different contexts without layout issues.


[
  {
    "discussion_id": "1132106601",
    "pr_number": 6952,
    "pr_file": "components/crud-web-apps/common/frontend/kubeflow-common-lib/projects/kubeflow/src/lib/status-info/status-info.component.scss",
    "created_at": "2023-03-10T08:55:50+00:00",
    "commented_code": ".panel-body {\n  background-color: rgba(0, 0, 0, 0.05);\n  border-radius: 4px;\n  padding: 1px;\n  display: flex;\n  font-size: 14px;\n  margin-top: 5px;",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1132106601",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6952,
        "pr_file": "components/crud-web-apps/common/frontend/kubeflow-common-lib/projects/kubeflow/src/lib/status-info/status-info.component.scss",
        "discussion_id": "1132106601",
        "commented_code": "@@ -0,0 +1,13 @@\n+.panel-body {\n+  background-color: rgba(0, 0, 0, 0.05);\n+  border-radius: 4px;\n+  padding: 1px;\n+  display: flex;\n+  font-size: 14px;\n+  margin-top: 5px;",
        "comment_created_at": "2023-03-10T08:55:50+00:00",
        "comment_author": "tasos-ale",
        "comment_body": "You have created a component that we might use in other WAs so it is better not to apply any styles that change its position. I suggest moving this margin in the component that is using the `status-info`.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1153302280",
    "pr_number": 7071,
    "pr_file": "components/centraldashboard-angular/frontend/src/app/pages/namespace-needed-page/namespace-needed-page.component.scss",
    "created_at": "2023-03-30T13:54:06+00:00",
    "commented_code": ":host {\n  flex: 1;",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1153302280",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7071,
        "pr_file": "components/centraldashboard-angular/frontend/src/app/pages/namespace-needed-page/namespace-needed-page.component.scss",
        "discussion_id": "1153302280",
        "commented_code": "@@ -0,0 +1,3 @@\n+:host {\n+  flex: 1;",
        "comment_created_at": "2023-03-30T13:54:06+00:00",
        "comment_author": "tasos-ale",
        "comment_body": "```suggestion\r\n  height: 100%;\r\n```\r\nSince we can have the same effect with `height` we can avoid assuming that component's parent has `display:flex`.",
        "pr_file_module": null
      }
    ]
  }
]
