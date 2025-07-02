---
title: Prefer external configuration
description: Design applications to use external configuration sources rather than
  hardcoding values directly in source code. This allows for configuration changes
  without requiring code modifications or redeployment.
repository: kubeflow/kubeflow
label: Configurations
language: Javascript
comments_count: 2
repository_stars: 15064
---

Design applications to use external configuration sources rather than hardcoding values directly in source code. This allows for configuration changes without requiring code modifications or redeployment.

When defining configurations that might change between environments or user preferences:
- Use mechanisms like ConfigMaps, environment variables, or properly namespaced storage keys
- Consider future extensibility in configuration design
- Prefer dynamic configuration that can be updated without code changes

For example, instead of hardcoding allowed namespaces:
```javascript
// Avoid this
export const ALL_NAMESPACES_ALLOWED_LIST = ['jupyter'];

// Prefer dynamic configuration loaded from an external source
export const ALL_NAMESPACES_ALLOWED_LIST = loadFromConfigMap('namespaces.allowed');
```

Similarly, when importing resources to support configurable features, consider importing complete libraries if it enables easier configuration through external sources:
```javascript
// This allows for configurable icons via ConfigMap without source code changes
import '@polymer/iron-icons/communication-icons.js';
```


[
  {
    "discussion_id": "996970427",
    "pr_number": 6674,
    "pr_file": "components/centraldashboard/public/components/namespace-selector.js",
    "created_at": "2022-10-17T11:58:08+00:00",
    "commented_code": "import {html, PolymerElement} from '@polymer/polymer/polymer-element.js';\n\nexport const ALL_NAMESPACES = 'All namespaces';\nexport const ALL_NAMESPACES_ALLOWED_LIST = ['jupyter'];",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "996970427",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6674,
        "pr_file": "components/centraldashboard/public/components/namespace-selector.js",
        "discussion_id": "996970427",
        "commented_code": "@@ -7,6 +7,12 @@ import '@polymer/paper-item/paper-item.js';\n \n import {html, PolymerElement} from '@polymer/polymer/polymer-element.js';\n \n+export const ALL_NAMESPACES = 'All namespaces';\n+export const ALL_NAMESPACES_ALLOWED_LIST = ['jupyter'];",
        "comment_created_at": "2022-10-17T11:58:08+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "@tasos-ale let's have this as an empty list initially, since we don't have an app that supports it at this point in time",
        "pr_file_module": null
      },
      {
        "comment_id": "996980605",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6674,
        "pr_file": "components/centraldashboard/public/components/namespace-selector.js",
        "discussion_id": "996970427",
        "commented_code": "@@ -7,6 +7,12 @@ import '@polymer/paper-item/paper-item.js';\n \n import {html, PolymerElement} from '@polymer/polymer/polymer-element.js';\n \n+export const ALL_NAMESPACES = 'All namespaces';\n+export const ALL_NAMESPACES_ALLOWED_LIST = ['jupyter'];",
        "comment_created_at": "2022-10-17T12:09:38+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "Ideally I'd like this to info (which web app supports all namespaces) to be transmitted via the common library, so that the dashboard can dynamically know if an app supports this once it loads it.\r\n\r\nBut we can do with hardcoding the urls for now. If in the future we see a bigger need for this we can look into it",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "551857860",
    "pr_number": 5474,
    "pr_file": "components/centraldashboard/public/components/resources/kubeflow-icons.js",
    "created_at": "2021-01-05T10:53:36+00:00",
    "commented_code": "*/\nimport '@polymer/iron-icon/iron-icon.js';\nimport '@polymer/iron-iconset-svg/iron-iconset-svg.js';\nimport '@polymer/iron-icons/communication-icons.js';",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "551857860",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5474,
        "pr_file": "components/centraldashboard/public/components/resources/kubeflow-icons.js",
        "discussion_id": "551857860",
        "commented_code": "@@ -4,6 +4,11 @@\n */\n import '@polymer/iron-icon/iron-icon.js';\n import '@polymer/iron-iconset-svg/iron-iconset-svg.js';\n+import '@polymer/iron-icons/communication-icons.js';",
        "comment_created_at": "2021-01-05T10:53:36+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "Do we need all of these new imports or only a subset of them?",
        "pr_file_module": null
      },
      {
        "comment_id": "553202269",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5474,
        "pr_file": "components/centraldashboard/public/components/resources/kubeflow-icons.js",
        "discussion_id": "551857860",
        "commented_code": "@@ -4,6 +4,11 @@\n */\n import '@polymer/iron-icon/iron-icon.js';\n import '@polymer/iron-iconset-svg/iron-iconset-svg.js';\n+import '@polymer/iron-icons/communication-icons.js';",
        "comment_created_at": "2021-01-07T09:19:26+00:00",
        "comment_author": "StefanoFioravanzo",
        "comment_body": "This is a good point but:\r\n\r\n1. I wouldn't know how to import just specific icons from these files, I had tried but didn't find a way\r\n2. Even if it was possible to import just specific icons, I would prefer to import these bundles so that people can then configure the sidebar with whatever icons they like (via ConfigMap) without having to change the source code",
        "pr_file_module": null
      },
      {
        "comment_id": "553287795",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5474,
        "pr_file": "components/centraldashboard/public/components/resources/kubeflow-icons.js",
        "discussion_id": "551857860",
        "commented_code": "@@ -4,6 +4,11 @@\n */\n import '@polymer/iron-icon/iron-icon.js';\n import '@polymer/iron-iconset-svg/iron-iconset-svg.js';\n+import '@polymer/iron-icons/communication-icons.js';",
        "comment_created_at": "2021-01-07T12:05:55+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "Makes sense, lets keep them then",
        "pr_file_module": null
      }
    ]
  }
]
