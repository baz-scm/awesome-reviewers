---
title: Standardize style scripts
description: Maintain consistent code style enforcement scripts across all projects
  by standardizing linting and formatting configurations in package.json. Use modern,
  supported tools instead of deprecated ones (like tslint).
repository: kubeflow/kubeflow
label: Code Style
language: Json
comments_count: 2
repository_stars: 15064
---

Maintain consistent code style enforcement scripts across all projects by standardizing linting and formatting configurations in package.json. Use modern, supported tools instead of deprecated ones (like tslint).

Every frontend project should include these standard scripts:

```json
{
  "scripts": {
    "lint-check": "ng lint",
    "lint": "ng lint --fix",
    "format:check": "prettier --check 'src/**/*.{js,ts,html,scss,css}' || node scripts/check-format-error.js"
  }
}
```

This approach ensures:
1. Consistent style enforcement across repositories
2. Both checking capabilities (`lint-check`, `format:check`) and auto-fixing options (`lint`)
3. Developer-friendly error messages when formatting fails
4. Alignment with established patterns in other repositories like Katib

When adding these scripts, make appropriate configurations in angular.json as needed to support them.


[
  {
    "discussion_id": "1039528459",
    "pr_number": 6786,
    "pr_file": "components/centraldashboard-angular/frontend/package.json",
    "created_at": "2022-12-05T12:27:32+00:00",
    "commented_code": "\"start\": \"ng serve --proxy-config proxy.conf.json\",\n    \"build\": \"ng build\",\n    \"watch\": \"ng build --watch --configuration development\",\n    \"test\": \"ng test\"\n    \"test\": \"ng test\",\n    \"test:prod\": \"ng test --no-watch --browsers ChromeHeadlessNoSandbox\",\n    \"tslint\": \"tslint -c tslint.json -p tsconfig.json\",",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1039528459",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6786,
        "pr_file": "components/centraldashboard-angular/frontend/package.json",
        "discussion_id": "1039528459",
        "commented_code": "@@ -6,7 +6,12 @@\n     \"start\": \"ng serve --proxy-config proxy.conf.json\",\n     \"build\": \"ng build\",\n     \"watch\": \"ng build --watch --configuration development\",\n-    \"test\": \"ng test\"\n+    \"test\": \"ng test\",\n+    \"test:prod\": \"ng test --no-watch --browsers ChromeHeadlessNoSandbox\",\n+    \"tslint\": \"tslint -c tslint.json -p tsconfig.json\",",
        "comment_created_at": "2022-12-05T12:27:32+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "Why do we introduce rules for `tslint`, which is getting deprecated?\r\n\r\nLet's instead have the following 2 rules:\r\n```json\r\n    \"lint-check\": \"ng lint\",\r\n    \"lint\": \"ng lint --fix\",\r\n```\r\nsimilarly to KWA https://github.com/kubeflow/katib/blob/master/pkg/new-ui/v1beta1/frontend/package.json#L12-L13\r\n\r\nWe might also need to make some small changes to the `angular.json`. Take a look at the previous effort for this in https://github.com/kubeflow/kubeflow/pull/6464",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1049832416",
    "pr_number": 6850,
    "pr_file": "components/crud-web-apps/tensorboards/frontend/package.json",
    "created_at": "2022-12-15T16:02:48+00:00",
    "commented_code": "\"test\": \"ng test\",\n    \"test:prod\": \"ng test --browsers=ChromeHeadless --watch=false\",\n    \"lint-check\": \"ng lint\",\n    \"lint\": \"ng lint --fix\"\n    \"lint\": \"ng lint --fix\",\n    \"format:check\": \"prettier --check 'src/**/*.{js,ts,html,scss,css}' || node scripts/check-format-error.js\",",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1049832416",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6850,
        "pr_file": "components/crud-web-apps/tensorboards/frontend/package.json",
        "discussion_id": "1049832416",
        "commented_code": "@@ -12,7 +12,9 @@\n     \"test\": \"ng test\",\n     \"test:prod\": \"ng test --browsers=ChromeHeadless --watch=false\",\n     \"lint-check\": \"ng lint\",\n-    \"lint\": \"ng lint --fix\"\n+    \"lint\": \"ng lint --fix\",\n+    \"format:check\": \"prettier --check 'src/**/*.{js,ts,html,scss,css}' || node scripts/check-format-error.js\",",
        "comment_created_at": "2022-12-15T16:02:48+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "I see that we don't have this script in TWA, like we do in Katib\r\nhttps://github.com/kubeflow/katib/tree/master/pkg/new-ui/v1beta1/frontend/scripts\r\n\r\nYet the action didn't fail. Why is that?",
        "pr_file_module": null
      },
      {
        "comment_id": "1049839951",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6850,
        "pr_file": "components/crud-web-apps/tensorboards/frontend/package.json",
        "discussion_id": "1049832416",
        "commented_code": "@@ -12,7 +12,9 @@\n     \"test\": \"ng test\",\n     \"test:prod\": \"ng test --browsers=ChromeHeadless --watch=false\",\n     \"lint-check\": \"ng lint\",\n-    \"lint\": \"ng lint --fix\"\n+    \"lint\": \"ng lint --fix\",\n+    \"format:check\": \"prettier --check 'src/**/*.{js,ts,html,scss,css}' || node scripts/check-format-error.js\",",
        "comment_created_at": "2022-12-15T16:09:09+00:00",
        "comment_author": "elenzio9",
        "comment_body": "Oh sorry I missed that. Should I add this script in TWA as well?",
        "pr_file_module": null
      },
      {
        "comment_id": "1049918468",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6850,
        "pr_file": "components/crud-web-apps/tensorboards/frontend/package.json",
        "discussion_id": "1049832416",
        "commented_code": "@@ -12,7 +12,9 @@\n     \"test\": \"ng test\",\n     \"test:prod\": \"ng test --browsers=ChromeHeadless --watch=false\",\n     \"lint-check\": \"ng lint\",\n-    \"lint\": \"ng lint --fix\"\n+    \"lint\": \"ng lint --fix\",\n+    \"format:check\": \"prettier --check 'src/**/*.{js,ts,html,scss,css}' || node scripts/check-format-error.js\",",
        "comment_created_at": "2022-12-15T17:02:25+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "OK I see what happened. `||` means that the second command (node script in this case) will NOT be run if the first part was successful. But the node script will run if the prettier check fails.\r\n\r\nThat script is just there to instruct users to run the formatting. Let's include it in this PR",
        "pr_file_module": null
      },
      {
        "comment_id": "1049930407",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6850,
        "pr_file": "components/crud-web-apps/tensorboards/frontend/package.json",
        "discussion_id": "1049832416",
        "commented_code": "@@ -12,7 +12,9 @@\n     \"test\": \"ng test\",\n     \"test:prod\": \"ng test --browsers=ChromeHeadless --watch=false\",\n     \"lint-check\": \"ng lint\",\n-    \"lint\": \"ng lint --fix\"\n+    \"lint\": \"ng lint --fix\",\n+    \"format:check\": \"prettier --check 'src/**/*.{js,ts,html,scss,css}' || node scripts/check-format-error.js\",",
        "comment_created_at": "2022-12-15T17:11:24+00:00",
        "comment_author": "elenzio9",
        "comment_body": "ACK! I just added it!",
        "pr_file_module": null
      }
    ]
  }
]
