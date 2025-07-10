---
title: Extract workflow scripts
description: Move complex scripts out of workflow YAML files into separate, dedicated
  script files in your repository. This practice significantly improves workflow maintainability,
  enables local testing of CI logic, and makes code reviews more effective.
repository: maplibre/maplibre-native
label: CI/CD
language: Yaml
comments_count: 4
repository_stars: 1411
---

Move complex scripts out of workflow YAML files into separate, dedicated script files in your repository. This practice significantly improves workflow maintainability, enables local testing of CI logic, and makes code reviews more effective.

**Benefits:**
- Scripts can be tested locally before committing changes
- Workflow files remain clean and readable
- Shell syntax errors can be caught before CI runs
- Scripts can be reused across multiple workflows
- Proper syntax highlighting in code editors

**Example:**

Instead of:
```yaml
# .github/workflows/example.yml
steps:
  - name: Upload external data for benchmark
    run: |
      mkdir -p /tmp/benchmark-data
      curl -L https://example.com/data.zip -o /tmp/benchmark-data/data.zip
      unzip /tmp/benchmark-data/data.zip -d /tmp/benchmark-data
      # many more lines of complex logic...
```

Prefer:
```yaml
# .github/workflows/example.yml
steps:
  - name: Upload external data for benchmark
    run: ./scripts/ci/upload-benchmark-data.sh
```

With script file:
```bash
# scripts/ci/upload-benchmark-data.sh
#!/bin/bash
set -euo pipefail

mkdir -p /tmp/benchmark-data
curl -L https://example.com/data.zip -o /tmp/benchmark-data/data.zip
unzip /tmp/benchmark-data/data.zip -d /tmp/benchmark-data
# many more lines of complex logic...
```

When scripts become more complex, consider also adding comments about their purpose and relationship to the build process to help other developers understand the workflow.