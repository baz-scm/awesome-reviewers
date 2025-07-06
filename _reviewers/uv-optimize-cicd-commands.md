---
title: Optimize CI/CD commands
description: 'Design CI/CD workflows to be efficient, consistent, and purposeful across
  all environments. When writing or modifying pipeline scripts:


  1. Batch related operations to minimize redundant commands and improve performance'
repository: astral-sh/uv
label: CI/CD
language: Yaml
comments_count: 5
repository_stars: 60322
---

Design CI/CD workflows to be efficient, consistent, and purposeful across all environments. When writing or modifying pipeline scripts:

1. Batch related operations to minimize redundant commands and improve performance
2. Apply security practices consistently across all deployment targets
3. Make intentional choices about caching strategies based on the pipeline's purpose
4. Document the reasoning behind non-obvious configuration decisions

For example, when working with Docker images, prefer batched operations:

```bash
# Inefficient: Multiple separate registry operations
for tag in $TAGS; do
  docker buildx imagetools create -t "${tag}" "${image}@${DIGEST}"
done

# Efficient: Batched operations per registry
readarray -t lines < <(grep "^${image}:" <<< "$TAGS"); tags=(); 
for line in "${lines[@]}"; do tags+=(-t "$line"); done
docker buildx imagetools create "${tags[@]}" "${image}@${DIGEST}"
```

For build caching strategies, be intentional about clean vs. incremental builds:

```yaml
# Explicitly using source files in cache key to ensure clean builds in release pipelines
- name: Docker Cargo caches
  uses: actions/cache@v4
  with:
    key: docker-cargo-caches-${{ matrix.platform }}-${{ hashFiles('Dockerfile', 'crates/**', 'Cargo.toml', 'Cargo.lock') }}
```