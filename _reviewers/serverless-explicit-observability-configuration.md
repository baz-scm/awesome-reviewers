---
title: explicit observability configuration
description: Ensure observability features are configured explicitly with clear documentation
  about their scope and impact. Avoid relying on implicit defaults or ambiguous configuration
  that could mislead users about what monitoring capabilities are being enabled or
  disabled.
repository: serverless/serverless
label: Observability
language: Markdown
comments_count: 2
repository_stars: 46810
---

Ensure observability features are configured explicitly with clear documentation about their scope and impact. Avoid relying on implicit defaults or ambiguous configuration that could mislead users about what monitoring capabilities are being enabled or disabled.

When documenting observability features, provide explicit YAML configuration examples that clearly show:
- What specific features are being controlled (monitoring, tracing, metrics)
- The scope of impact (service-level vs dashboard-level features)
- Clear examples for different environments/stages

Example of good explicit configuration:
```yaml
stages:
  prod:
    observability: true # turn on observability in the "prod" Stage.
  dev:
    observability: true # turn on observability in the "dev" Stage.
  default:
    observability: false # turn off observability for all other Stages.
```

Avoid suggesting broad configuration changes (like removing `app` property) when the intent is to disable only specific observability features, as this can unintentionally disable other dashboard functionality.