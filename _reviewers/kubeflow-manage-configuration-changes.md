---
title: Manage configuration changes
description: 'Carefully manage configuration file changes to ensure consistency and
  minimize unintended impacts across your project. When modifying configuration files:'
repository: kubeflow/kubeflow
label: Configurations
language: Json
comments_count: 3
repository_stars: 15064
---

Carefully manage configuration file changes to ensure consistency and minimize unintended impacts across your project. When modifying configuration files:

1) Ensure compiler settings match runtime requirements - update targets to support required language features (like changing TypeScript target to "es2020" to support BigInt in Node.js 12)

2) Maintain consistent paths and settings across related configurations to prevent deployment issues

```json
// Example: Consistent paths in build scripts
"scripts": {
  "start": "ng serve --base-href /tensorboards/ --deploy-url /tensorboards/",
  "build": "ng build --prod --base-href /tensorboards/ --deploy-url static/"
}
```

3) Isolate high-impact configuration changes (like dependency updates that affect package-lock.json) into separate PRs to maintain reviewability and minimize unintended side effects


[
  {
    "discussion_id": "774008435",
    "pr_number": 6258,
    "pr_file": "components/centraldashboard/tsconfig.json",
    "created_at": "2021-12-22T16:15:56+00:00",
    "commented_code": "\"compilerOptions\":{\n        \"module\":\"commonjs\",\n        \"esModuleInterop\":true,\n        \"target\":\"es6\",\n        \"target\":\"es2020\",\n        \"noImplicitAny\":true,",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "774008435",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6258,
        "pr_file": "components/centraldashboard/tsconfig.json",
        "discussion_id": "774008435",
        "commented_code": "@@ -2,7 +2,7 @@\n     \"compilerOptions\":{\n         \"module\":\"commonjs\",\n         \"esModuleInterop\":true,\n-        \"target\":\"es6\",\n+        \"target\":\"es2020\",\n         \"noImplicitAny\":true,",
        "comment_created_at": "2021-12-22T16:15:56+00:00",
        "comment_author": "haoxins",
        "comment_body": "Change to `es2020` because of the latest K8s Node.js client used `BigInt` (Node.js 12 supported).",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "593452634",
    "pr_number": 5693,
    "pr_file": "components/crud-web-apps/tensorboards/frontend/package.json",
    "created_at": "2021-03-12T21:11:39+00:00",
    "commented_code": "\"scripts\": {\n    \"ng\": \"ng\",\n    \"start\": \"npm run copyLibAssets && ng serve --base-href /tensorboard/ --deploy-url /tensorboard/\",\n    \"build\": \"npm run copyLibAssets && ng build --prod --base-href /tensorboard/ --deploy-url /tensorboard/static/\",\n    \"build\": \"npm run copyLibAssets && ng build --prod --base-href /tensorboards/ --deploy-url static/\",",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "593452634",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5693,
        "pr_file": "components/crud-web-apps/tensorboards/frontend/package.json",
        "discussion_id": "593452634",
        "commented_code": "@@ -4,7 +4,7 @@\n   \"scripts\": {\n     \"ng\": \"ng\",\n     \"start\": \"npm run copyLibAssets && ng serve --base-href /tensorboard/ --deploy-url /tensorboard/\",\n-    \"build\": \"npm run copyLibAssets && ng build --prod --base-href /tensorboard/ --deploy-url /tensorboard/static/\",\n+    \"build\": \"npm run copyLibAssets && ng build --prod --base-href /tensorboards/ --deploy-url static/\",",
        "comment_created_at": "2021-03-12T21:11:39+00:00",
        "comment_author": "davidspek",
        "comment_body": "In the line above the base-href is `/tensorboard/` instead of `/tensorboards/` which it is here. ",
        "pr_file_module": null
      },
      {
        "comment_id": "595241172",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5693,
        "pr_file": "components/crud-web-apps/tensorboards/frontend/package.json",
        "discussion_id": "593452634",
        "commented_code": "@@ -4,7 +4,7 @@\n   \"scripts\": {\n     \"ng\": \"ng\",\n     \"start\": \"npm run copyLibAssets && ng serve --base-href /tensorboard/ --deploy-url /tensorboard/\",\n-    \"build\": \"npm run copyLibAssets && ng build --prod --base-href /tensorboard/ --deploy-url /tensorboard/static/\",\n+    \"build\": \"npm run copyLibAssets && ng build --prod --base-href /tensorboards/ --deploy-url static/\",",
        "comment_created_at": "2021-03-16T14:48:02+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "I'm not sure I understand what the question or suggested change is here. Could you rephrase this?",
        "pr_file_module": null
      },
      {
        "comment_id": "595266057",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5693,
        "pr_file": "components/crud-web-apps/tensorboards/frontend/package.json",
        "discussion_id": "593452634",
        "commented_code": "@@ -4,7 +4,7 @@\n   \"scripts\": {\n     \"ng\": \"ng\",\n     \"start\": \"npm run copyLibAssets && ng serve --base-href /tensorboard/ --deploy-url /tensorboard/\",\n-    \"build\": \"npm run copyLibAssets && ng build --prod --base-href /tensorboard/ --deploy-url /tensorboard/static/\",\n+    \"build\": \"npm run copyLibAssets && ng build --prod --base-href /tensorboards/ --deploy-url static/\",",
        "comment_created_at": "2021-03-16T15:12:21+00:00",
        "comment_author": "davidspek",
        "comment_body": "There is an inconsistency in the usage of `--base-href /tensorboard/ --deploy-url /tensorboard/\"` on Line 6 and `--base-href /tensorboards/` on Line 7.",
        "pr_file_module": null
      },
      {
        "comment_id": "595303549",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5693,
        "pr_file": "components/crud-web-apps/tensorboards/frontend/package.json",
        "discussion_id": "593452634",
        "commented_code": "@@ -4,7 +4,7 @@\n   \"scripts\": {\n     \"ng\": \"ng\",\n     \"start\": \"npm run copyLibAssets && ng serve --base-href /tensorboard/ --deploy-url /tensorboard/\",\n-    \"build\": \"npm run copyLibAssets && ng build --prod --base-href /tensorboard/ --deploy-url /tensorboard/static/\",\n+    \"build\": \"npm run copyLibAssets && ng build --prod --base-href /tensorboards/ --deploy-url static/\",",
        "comment_created_at": "2021-03-16T15:51:35+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "I see what you mean. The `start` script should be completely removed, since the users should run the UI locally with `build:watch` for now.\r\n\r\nI'll push a commit to remove this script",
        "pr_file_module": null
      },
      {
        "comment_id": "595369242",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5693,
        "pr_file": "components/crud-web-apps/tensorboards/frontend/package.json",
        "discussion_id": "593452634",
        "commented_code": "@@ -4,7 +4,7 @@\n   \"scripts\": {\n     \"ng\": \"ng\",\n     \"start\": \"npm run copyLibAssets && ng serve --base-href /tensorboard/ --deploy-url /tensorboard/\",\n-    \"build\": \"npm run copyLibAssets && ng build --prod --base-href /tensorboard/ --deploy-url /tensorboard/static/\",\n+    \"build\": \"npm run copyLibAssets && ng build --prod --base-href /tensorboards/ --deploy-url static/\",",
        "comment_created_at": "2021-03-16T17:02:35+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "Added a commit that removes the unused npm script",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "612292983",
    "pr_number": 5823,
    "pr_file": "components/crud-web-apps/jupyter/frontend/package.json",
    "created_at": "2021-04-13T09:39:46+00:00",
    "commented_code": "\"@fortawesome/free-brands-svg-icons\": \"^5.12.0\",\n    \"@fortawesome/free-solid-svg-icons\": \"^5.12.0\",\n    \"@kubernetes/client-node\": \"^0.12.2\",\n    \"hammerjs\": \"^2.0.8\",\n    \"date-fns\": \"^1.29.0\",\n    \"lodash-es\": \"^4.17.11\",",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "612292983",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5823,
        "pr_file": "components/crud-web-apps/jupyter/frontend/package.json",
        "discussion_id": "612292983",
        "commented_code": "@@ -32,10 +32,10 @@\n     \"@fortawesome/free-brands-svg-icons\": \"^5.12.0\",\n     \"@fortawesome/free-solid-svg-icons\": \"^5.12.0\",\n     \"@kubernetes/client-node\": \"^0.12.2\",\n-    \"hammerjs\": \"^2.0.8\",\n     \"date-fns\": \"^1.29.0\",\n-    \"lodash-es\": \"^4.17.11\",",
        "comment_created_at": "2021-04-13T09:39:46+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "Let's exclude this change from this PR and keep the touched lines to the minimum. This will also remove the 15.000 modified lines to the `package-lock.json` because of this change.\r\n\r\nAlthough I'd like to progressively replace the use of `lodash` with `lodash-es`, but until I get to it we can remove this from the `package.json`, but lets just do it in another PR.",
        "pr_file_module": null
      }
    ]
  }
]
