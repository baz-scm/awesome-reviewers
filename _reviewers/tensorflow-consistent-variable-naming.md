---
title: Consistent variable naming
description: Use ALL_CAPS for constants and environment variables in shell scripts,
  and reference these variables consistently throughout the script with proper quoting.
  This improves code readability and prevents errors when handling paths with spaces.
repository: tensorflow/tensorflow
label: Naming Conventions
language: Shell
comments_count: 2
repository_stars: 190625
---

Use ALL_CAPS for constants and environment variables in shell scripts, and reference these variables consistently throughout the script with proper quoting. This improves code readability and prevents errors when handling paths with spaces.

Example:
```bash
# Correct
OUTPUT_FILE=tf_env.txt
PYTHON_BIN_PATH="$(which python || which python3 || die "Cannot find Python binary")"

# Then reference consistently
"${PYTHON_BIN_PATH}" -c 'import sys; print(sys.version_info[:])'

# Incorrect
python_bin_path=$(which python || which python3 || die "Cannot find Python binary")
python -c 'import sys; print(sys.version_info[:])'  # Inconsistent reference
```

Using a consistent naming convention makes scripts more maintainable and helps other developers understand which values are constants. Double-quoting variables (like `"${PYTHON_BIN_PATH}"`) ensures that paths with spaces are handled correctly.