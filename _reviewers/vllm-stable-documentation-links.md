---
title: Stable documentation links
description: 'Ensure all documentation links are stable, consistent, and correctly
  targeted to improve navigation and long-term maintainability:


  1. **Use stable references**: Always link to stable release tags or specific commit
  hashes rather than volatile branches like `master` or `main`:'
repository: vllm-project/vllm
label: Documentation
language: Markdown
comments_count: 6
repository_stars: 51730
---

Ensure all documentation links are stable, consistent, and correctly targeted to improve navigation and long-term maintainability:

1. **Use stable references**: Always link to stable release tags or specific commit hashes rather than volatile branches like `master` or `main`:
   ```diff
   - kubectl apply -f https://raw.githubusercontent.com/ray-project/kuberay/refs/heads/master/ray-operator/config/samples/vllm/ray-service.vllm.yaml
   + kubectl apply -f https://raw.githubusercontent.com/ray-project/kuberay/vX.Y.Z/ray-operator/config/samples/vllm/ray-service.vllm.yaml
   ```

2. **Maintain consistent file extensions**: Use consistent file extensions (.md or .html) throughout documentation links, preferring `.md` for markdown source files:
   ```diff
   - See also: [full example](../examples/online_serving/structured_outputs.html)
   + See also: [full example](../examples/online_serving/structured_outputs.md)
   ```

3. **Verify relative paths**: Ensure relative paths resolve correctly within the documentation structure by testing links in the built documentation.

4. **Use standardized link syntax**: Follow project conventions for link formatting, such as using autolink syntax:
   ```diff
   - While ongoing efforts like [#17419](https://github.com/vllm-project/vllm/issues/17419)
   + While ongoing efforts like <gh-issue:17419>
   ```

5. **Target specific sections**: When linking to pages with tabs or complex navigation, link directly to the specific section or tab to improve user experience.