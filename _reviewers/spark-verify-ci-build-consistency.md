---
title: Verify CI build consistency
description: Ensure CI pipelines thoroughly verify build outputs and maintain consistency
  across different build tools and configurations. This prevents broken builds from
  reaching contributors and ensures reliable deployment artifacts.
repository: apache/spark
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 41554
---

Ensure CI pipelines thoroughly verify build outputs and maintain consistency across different build tools and configurations. This prevents broken builds from reaching contributors and ensures reliable deployment artifacts.

Key practices:
1. **Cross-tool verification**: When using multiple build tools (Maven, SBT), verify that both produce consistent, working artifacts
2. **Proper build phases**: Use correct Maven lifecycle phases (e.g., `package test` instead of just `test`) to ensure proper classpath resolution
3. **Rigorous output testing**: Test the actual distribution artifacts, not just intermediate build outputs

Example from Maven workflow:
```yaml
# Ensure proper Maven phase ordering for integration tests
./build/mvn $MAVEN_CLI_OPTS -pl sql/connect/client/jvm,sql/connect/client/integration-tests,sql/connect/common,sql/connect/server package test -fae
```

This approach protects contributors' daily development by catching build inconsistencies early and making it easier to identify offending commits when builds break.