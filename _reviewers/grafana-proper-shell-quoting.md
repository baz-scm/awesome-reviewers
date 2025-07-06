---
title: Proper shell quoting
description: 'Always use proper quoting in shell scripts (especially GitHub Actions
  workflows) to prevent word splitting, globbing, and ensure correct variable expansion:'
repository: grafana/grafana
label: Code Style
language: Yaml
comments_count: 5
repository_stars: 68825
---

Always use proper quoting in shell scripts (especially GitHub Actions workflows) to prevent word splitting, globbing, and ensure correct variable expansion:

1. Use double quotes around variable expansions and command substitutions to prevent word splitting:
   ```bash
   # Incorrect
   go list -f '{{.Dir}}/...' -m | xargs go test -short -covermode=atomic -timeout=5m
   
   # Correct
   go list -f '{{.Dir}}/...' -m | xargs bash -c "go test -short -covermode=atomic -timeout=5m"
   ```

2. Use double quotes (not single quotes) when you need variable expansion:
   ```bash
   # Incorrect - variables won't expand in single quotes
   echo 'Value: $SOME_VAR'
   
   # Correct - allows variable expansion
   echo "Value: $SOME_VAR"
   ```

3. Always quote variables in conditions and arguments to prevent unexpected behavior:
   ```bash
   # Incorrect
   if [ $status == success ]; then
   
   # Correct
   if [ "$status" == "success" ]; then
   ```

These practices prevent common shell scripting errors that tools like shellcheck will flag (SC2046, SC2016, SC2086), resulting in more robust and predictable scripts.