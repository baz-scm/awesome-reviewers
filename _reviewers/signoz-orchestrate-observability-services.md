---
title: orchestrate observability services
description: When setting up observability infrastructure in build systems, use proper
  dependency management and descriptive naming. Define service dependencies explicitly
  rather than embedding commands, and use specific names that clearly identify the
  observability tools being orchestrated.
repository: SigNoz/signoz
label: Observability
language: Other
comments_count: 2
repository_stars: 23369
---

When setting up observability infrastructure in build systems, use proper dependency management and descriptive naming. Define service dependencies explicitly rather than embedding commands, and use specific names that clearly identify the observability tools being orchestrated.

For example, instead of creating a target with embedded commands:
```makefile
devenv-up: ## Start the dev stack
	@cd .devenv/docker/clickhouse; docker compose up -d
	@cd .devenv/docker/otel-collector; docker compose up -d
```

Use Make dependencies with descriptive target names:
```makefile
devenv-up: devenv-clickhouse devenv-signoz-otel-collector

devenv-signoz-otel-collector: ## Run signoz-otel-collector in devenv
	@cd .devenv/docker/otel-collector; docker compose up -d
```

This approach makes the observability stack setup more maintainable, allows for selective service startup, and clearly communicates which specific observability tools are being used.