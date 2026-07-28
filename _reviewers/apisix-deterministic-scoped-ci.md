---
title: Deterministic, scoped CI
description: 'CI jobs that build artifacts must be deterministic and guarded, and
  CI tests must be scoped to avoid unnecessary heavy work.


  **Apply these rules**

  1) **Guard CI assumptions (fail loudly):** If a build-time tweak is required (e.g.,
  removing -march=native leakage), make the script error when the expected input/state
  isn’t found—never allow a “no-op” edit...'
repository: apache/apisix
label: CI/CD
language: Shell
comments_count: 2
repository_stars: 16922
---

CI jobs that build artifacts must be deterministic and guarded, and CI tests must be scoped to avoid unnecessary heavy work.

**Apply these rules**
1) **Guard CI assumptions (fail loudly):** If a build-time tweak is required (e.g., removing -march=native leakage), make the script error when the expected input/state isn’t found—never allow a “no-op” edit that silently produces a different binary.
2) **Keep scripts portable and version-stable:** Use portable tooling options (e.g., sed -i.bak) and pin dependency/build versions so pattern matches don’t break unexpectedly.
3) **Avoid rebuilding heavyweight dependencies in-line:** Prefer prebuilt images/artifacts, caching, or reusing a prior build.
4) **Scope expensive tests by change set:** Move costly jobs (like Docker image build + integration runs) into separate workflows/jobs and run them only when relevant files change.

**Example: fail loudly + portable edit (bash)**
```bash
set -euo pipefail
# ... obtain/extract source at a pinned version ...
file="CMakeLists.txt"
needle='add_compile_options(-march=native)'

# Portable in-place edit with backup, and verify the line existed.
if ! grep -qF "${needle}" "${file}"; then
  echo "Expected line not found: ${needle} (refusing to build native-leaking artifact)" >&2
  exit 1
fi
sed -i.bak "/${needle//\//\\\/}/d" "${file}"
```

**Example: run expensive workflow only when relevant paths change (GitHub Actions)**
```yaml
on:
  push:
    paths:
      - 'ops.lua'
      - 'docker-entrypoint.sh'
      - 't/cli/test_standalone_docker.sh'
      - 'ci/**'
```

This standard prevents silent build drift and keeps pipelines fast by doing the minimum necessary work per change.