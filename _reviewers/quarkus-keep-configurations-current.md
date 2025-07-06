---
title: Keep configurations current
description: Always use the latest stable and supported versions in configuration
  files. This applies to runtime environments, build plugins, and dependencies. Outdated
  configurations can limit functionality, miss security updates, or prevent access
  to newer features.
repository: quarkusio/quarkus
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 14667
---

Always use the latest stable and supported versions in configuration files. This applies to runtime environments, build plugins, and dependencies. Outdated configurations can limit functionality, miss security updates, or prevent access to newer features.

For runtime environments:
```yaml
# AVOID
Properties:
  Handler: io.quarkus.funqy.lambda.FunqyStreamHandler::handleRequest
  Runtime: java8

# PREFER
Properties:
  Handler: io.quarkus.funqy.lambda.FunqyStreamHandler::handleRequest
  Runtime: java17  # Or java21 if supported
```

For build plugins and dependencies, regularly evaluate if newer alternatives provide better functionality or consolidate multiple tools:
- Consider tools that solve multiple problems (e.g., "spot covering impsort-maven-plugin")
- Verify license compatibility when introducing new configuration dependencies
- Look for options that "go beyond whitespaces fixing real issues and flaws"

Periodically review all configuration files as part of your maintenance routine to ensure they reflect current best practices and supported versions.