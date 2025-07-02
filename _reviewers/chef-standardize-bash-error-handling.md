---
title: Standardize bash error-handling
description: Always use `set -eou pipefail` at the beginning of bash scripts to ensure
  consistent and robust error handling. This combination ensures scripts fail immediately
  on errors (`-e`), treat unset variables as errors (`-u`), and properly handle pipeline
  failures (`-o pipefail`), preventing silent failures and making debugging easier.
repository: chef/chef
label: Error Handling
language: Shell
comments_count: 2
repository_stars: 7860
---

Always use `set -eou pipefail` at the beginning of bash scripts to ensure consistent and robust error handling. This combination ensures scripts fail immediately on errors (`-e`), treat unset variables as errors (`-u`), and properly handle pipeline failures (`-o pipefail`), preventing silent failures and making debugging easier.

```bash
# Good practice
#!/bin/bash
set -eou pipefail

# Rest of your script
```


[
  {
    "discussion_id": "2142594793",
    "pr_number": 15049,
    "pr_file": ".expeditor/build-docker-images.sh",
    "created_at": "2025-06-12T12:21:24+00:00",
    "commented_code": "#! /bin/bash\nset -eux -o pipefail",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "2142594793",
        "repo_full_name": "chef/chef",
        "pr_number": 15049,
        "pr_file": ".expeditor/build-docker-images.sh",
        "discussion_id": "2142594793",
        "commented_code": "@@ -1,6 +1,9 @@\n #! /bin/bash\n set -eux -o pipefail",
        "comment_created_at": "2025-06-12T12:21:24+00:00",
        "comment_author": "sean-sype-simmons",
        "comment_body": "please update to: `set -eou pipefail` ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2142595017",
    "pr_number": 15049,
    "pr_file": ".expeditor/docker-manifest-create.sh",
    "created_at": "2025-06-12T12:21:31+00:00",
    "commented_code": "set -eu -o pipefail",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "2142595017",
        "repo_full_name": "chef/chef",
        "pr_number": 15049,
        "pr_file": ".expeditor/docker-manifest-create.sh",
        "discussion_id": "2142595017",
        "commented_code": "@@ -2,6 +2,8 @@\n set -eu -o pipefail",
        "comment_created_at": "2025-06-12T12:21:31+00:00",
        "comment_author": "sean-sype-simmons",
        "comment_body": "please update to: `set -eou pipefail` ",
        "pr_file_module": null
      }
    ]
  }
]
