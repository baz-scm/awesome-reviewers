---
title: Match reference names
description: Ensure that filenames and paths referenced in scripts, commands, or configuration
  files exactly match the actual names of the files they reference. Name mismatches
  between references and actual files can cause commands to fail during execution.
repository: vllm-project/vllm
label: Naming Conventions
language: Other
comments_count: 2
repository_stars: 51730
---

Ensure that filenames and paths referenced in scripts, commands, or configuration files exactly match the actual names of the files they reference. Name mismatches between references and actual files can cause commands to fail during execution.

For example, in a Justfile, the reference:
```
python {{vllm-directory}}benchmarks/benchmark_one_concurrent_req.py
```
should be changed to:
```
python {{vllm-directory}}benchmarks/benchmark_one_concurrent.py
```
to match the actual filename.

Always verify references against the actual filesystem structure before committing code to prevent runtime failures. This is especially important in build scripts, makefiles, and configuration files where a simple typo can break the entire workflow.