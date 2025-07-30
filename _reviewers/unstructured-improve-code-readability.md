---
title: improve code readability
description: Format code to enhance readability and maintainability by breaking long
  lines and extracting repeated values into variables. Long command lines with multiple
  parameters should be split across multiple lines with proper line continuation,
  placing each parameter on its own line. When the same value (like URLs, paths, or
  configuration strings) appears multiple...
repository: Unstructured-IO/unstructured
label: Code Style
language: Shell
comments_count: 2
repository_stars: 12117
---

Format code to enhance readability and maintainability by breaking long lines and extracting repeated values into variables. Long command lines with multiple parameters should be split across multiple lines with proper line continuation, placing each parameter on its own line. When the same value (like URLs, paths, or configuration strings) appears multiple times, extract it into a clearly named variable at the top of the file.

Example of improved formatting:
```bash
# Extract repeated URL base
BASE_URL="https://ingest-test-azure-cognitive-search.search.windows.net"

# Break long command lines for readability
PYTHONPATH=${PYTHONPATH:-.} "$RUN_SCRIPT" \
  --reprocess \
  --input-path example-docs/fake-memo.pdf \
  --work-dir "$WORK_DIR" \
  --chunking-strategy by_title \
  --chunk-combine-text-under-n-chars 150 \
  --chunk-new-after-n-chars 1500 \
  --chunk-max-characters 2500 \
  --chunk-multipage-sections \
  --chunk-no-include-orig-elements
```

This approach reduces duplication, makes the code easier to modify, and significantly improves readability by avoiding overly long lines that are difficult to scan and understand.