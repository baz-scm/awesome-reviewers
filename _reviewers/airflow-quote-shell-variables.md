---
title: Quote shell variables
description: Always quote shell script variable expansions using double quotes to
  prevent word splitting issues and ensure consistent behavior. This is particularly
  important in conditionals and when passing variables as command arguments.
repository: apache/airflow
label: Code Style
language: Shell
comments_count: 2
repository_stars: 40858
---

Always quote shell script variable expansions using double quotes to prevent word splitting issues and ensure consistent behavior. This is particularly important in conditionals and when passing variables as command arguments.

Bad:
```bash
rm -rf /usr/local/lib/python${PYTHON_MAJOR_MINOR_VERSION}/site-packages/
if [[ ${UPGRADE_SQLALCHEMY=} != "true" ]]; then
```

Good:
```bash
rm -rf /usr/local/lib/python"${PYTHON_MAJOR_MINOR_VERSION}"/site-packages/
if [[ "${UPGRADE_SQLALCHEMY}" != "true" ]]; then
```

Unquoted variables can lead to unexpected behavior when they contain spaces, are empty, or include special characters. Consistently applying proper quoting improves script robustness and prevents subtle bugs that might only appear in edge cases.