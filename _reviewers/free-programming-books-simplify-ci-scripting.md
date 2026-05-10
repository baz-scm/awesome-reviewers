---
title: Simplify CI scripting
description: 'Keep CI/CD workflow steps readable and maintainable by consolidating
  repeated commands and using basic shell utilities for log processing.


  Apply these rules:'
repository: EbookFoundation/free-programming-books
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 388003
---

Keep CI/CD workflow steps readable and maintainable by consolidating repeated commands and using basic shell utilities for log processing.

Apply these rules:
- Consolidate repeated tool invocations into one command where supported (e.g., pass multiple paths at once).
- For creating empty files, use `touch file` rather than `cat > file`.
- For simple transformations/filters of a log, prefer bash + coreutils (e.g., `sed`, `uniq`) over adding a JavaScript cleanup step.

Example (PR log cleanup + artifact):
```sh
# Run lint and capture output
fpb-lint ./books/ &>> output.log || echo "Analyzing..."
fpb-lint ./casts/ &>> output.log || echo "Analyzing..."
fpb-lint ./courses/ &>> output.log || echo "Analyzing..."
fpb-lint ./more/ &>> output.log || echo "Analyzing..."

# Prepare artifact
mkdir -p ./pr
echo "$PR_URL" > ./pr/PRurl

# Bash cleanup (single-line transformation + dedupe)
cat output.log | sed -E 's:/home/runner/work/free-programming-books/|⚠.+::' | uniq > ./pr/error.log
```
If the cleanup logic becomes complex enough that shell becomes unreadable, then (and only then) consider a script—but default to the simplest working approach.