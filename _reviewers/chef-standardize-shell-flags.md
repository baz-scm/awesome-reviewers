---
title: Standardize shell flags
description: 'Always use `set -eou pipefail` at the beginning of shell scripts to
  ensure consistent error handling and behavior across the codebase. This combination
  provides important safety guarantees:'
repository: chef/chef
label: Code Style
language: Shell
comments_count: 3
repository_stars: 7860
---

Always use `set -eou pipefail` at the beginning of shell scripts to ensure consistent error handling and behavior across the codebase. This combination provides important safety guarantees:

- `-e`: Exit immediately if any command exits with non-zero status
- `-o`: Error on undefined variables instead of treating them as empty
- `-u`: Treat unset variables as an error
- `pipefail`: Return value of a pipeline is the status of the last command to exit with non-zero status

Example:
```sh
# Incorrect
set -eu -o pipefail
# or 
set -evx

# Correct
set -eou pipefail
```

This standard helps prevent subtle bugs caused by unhandled errors or undefined variables and makes scripts more robust and predictable.


[
  {
    "discussion_id": "2142595259",
    "pr_number": 15049,
    "pr_file": ".expeditor/promote-docker-images.sh",
    "created_at": "2025-06-12T12:21:39+00:00",
    "commented_code": "set -eu -o pipefail",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "2142595259",
        "repo_full_name": "chef/chef",
        "pr_number": 15049,
        "pr_file": ".expeditor/promote-docker-images.sh",
        "discussion_id": "2142595259",
        "commented_code": "@@ -2,6 +2,8 @@\n set -eu -o pipefail",
        "comment_created_at": "2025-06-12T12:21:39+00:00",
        "comment_author": "sean-sype-simmons",
        "comment_body": "please update to: `set -eou pipefail` ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2142596054",
    "pr_number": 15049,
    "pr_file": ".expeditor/update_dep.sh",
    "created_at": "2025-06-12T12:22:04+00:00",
    "commented_code": "set -evx",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "2142596054",
        "repo_full_name": "chef/chef",
        "pr_number": 15049,
        "pr_file": ".expeditor/update_dep.sh",
        "discussion_id": "2142596054",
        "commented_code": "@@ -11,6 +11,9 @@\n \n set -evx",
        "comment_created_at": "2025-06-12T12:22:04+00:00",
        "comment_author": "sean-sype-simmons",
        "comment_body": "please update to: `set -eou pipefail` ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2142596218",
    "pr_number": 15049,
    "pr_file": ".expeditor/update_dockerfile.sh",
    "created_at": "2025-06-12T12:22:09+00:00",
    "commented_code": "############################################################################\n\nset -evx",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "2142596218",
        "repo_full_name": "chef/chef",
        "pr_number": 15049,
        "pr_file": ".expeditor/update_dockerfile.sh",
        "discussion_id": "2142596218",
        "commented_code": "@@ -10,5 +10,7 @@\n ############################################################################\n \n set -evx",
        "comment_created_at": "2025-06-12T12:22:09+00:00",
        "comment_author": "sean-sype-simmons",
        "comment_body": "please update to: `set -eou pipefail` ",
        "pr_file_module": null
      }
    ]
  }
]
