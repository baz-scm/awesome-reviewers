---
title: Consolidate configuration files
description: Avoid proliferating ad-hoc configuration files (e.g. new docker-compose
  variants) when existing ones can be extended or reused. Before adding a new config
  file, check whether an existing one (like `docker-compose.yml` for the full stack
  or `docker-compose-dev.yml` for infra-only) already serves that purpose, and extend
  it rather than creating a...
repository: Helicone/helicone
label: Configurations
language: Yaml
comments_count: 3
repository_stars: 6248
---

Avoid proliferating ad-hoc configuration files (e.g. new docker-compose variants) when existing ones can be extended or reused. Before adding a new config file, check whether an existing one (like `docker-compose.yml` for the full stack or `docker-compose-dev.yml` for infra-only) already serves that purpose, and extend it rather than creating a near-duplicate. If multiple files share overlapping settings, factor out common pieces (e.g. a `docker-compose.infra.yml` + `docker-compose.helicone.yml` combined via `-f` flags, or a single file using `--profile`) so there is one source of truth and less maintenance burden.

When you do need to change shared/default configuration values (env vars, credentials, ports, etc.) in a file other developers rely on, verify the change doesn't break existing local setups. For example, changing `CLICKHOUSE_DEFAULT_USER` to `CLICKHOUSE_USER`/`CLICKHOUSE_PASSWORD` broke the default no-password local setup other developers depended on — such changes should be tested against a clean checkout before merging, and reverted or isolated into an environment-specific override if they aren't universally needed.

If cleanup of duplicated config files or deeper refactors (DRYing compose files) can't be done immediately, file a tracked follow-up ticket rather than leaving redundant files in the repo indefinitely.