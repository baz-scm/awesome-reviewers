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
