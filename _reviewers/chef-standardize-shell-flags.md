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
