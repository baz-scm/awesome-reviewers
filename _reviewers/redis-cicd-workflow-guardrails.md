---
title: CI/CD Workflow Guardrails
description: When building or modifying CI/CD GitHub Actions workflows, structure
  them as an explicit DAG of artifact-driven jobs and guard execution to prevent fork/irrelevant-context
  failures.
repository: redis/redis
label: CI/CD
language: Yaml
comments_count: 7
repository_stars: 74261
---

When building or modifying CI/CD GitHub Actions workflows, structure them as an explicit DAG of artifact-driven jobs and guard execution to prevent fork/irrelevant-context failures.

**Standards**
1) **Gate by repo once, with correct allowlist**
- Prefer workflow/job-level `if: github.repository == '<upstream>'` (or a clearly maintained allowlist) so jobs don’t run in forks where secrets/tokens or release logic would fail.

2) **Make ordering explicit with `needs`**
- If a job uses outputs/artifacts from another job, declare `needs` and consume `needs.<job>.outputs`.
- Ensure a “summary/finalization” job uses `if: always()` and has the needed `needs: [...]` so it can run even when earlier jobs are skipped.

3) **Use job outputs/env, not ad-hoc shell env unless needed**
- Export values via `outputs` on the producing job (computed from steps) and reference them in downstream jobs.

4) **Add lightweight artifact validation**
- For release workflows that create tarballs/binaries, include a basic sanity check (e.g., checksum and/or size range) to catch malformed or unexpectedly changed artifacts early.

5) **Keep CI dependencies aligned with what you actually run**
- Don’t install or configure toolchains/flags (e.g., ASAN/cpp toolchain) unless that CI job truly exercises them.

**Example pattern**
```yaml
jobs:
  extract:
    if: github.repository == 'redis/redis'
    runs-on: ubuntu-latest
    outputs:
      tag: ${{ steps.info.outputs.tag }}
    steps:
      - id: info
        run: echo "tag=v1.2.3" >> "$GITHUB_OUTPUT"

  create-artifact:
    needs: extract
    runs-on: ubuntu-latest
    outputs:
      sha256: ${{ steps.checksum.outputs.sha256 }}
    steps:
      - run: ./utils/releasetools/01_create_tarball.sh "${{ needs.extract.outputs.tag }}"
      - id: checksum
        run: |
          TARBALL="/tmp/redis-${{ needs.extract.outputs.tag }}.tar.gz"
          SHA256=$(shasum -a 256 "$TARBALL" | cut -d' ' -f1)
          echo "sha256=$SHA256" >> "$GITHUB_OUTPUT"

  summary:
    needs: [extract, create-artifact]
    if: always()
    runs-on: ubuntu-latest
    steps:
      - run: echo "Pipeline completed (may be partially skipped)."
```

Applying these rules prevents cascading failures on forks, makes workflow behavior predictable, and improves reliability of release automation by validating what you produce before you publish it.