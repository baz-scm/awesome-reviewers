---
title: avoid hardcoded configuration
description: Avoid hardcoding configuration values directly in code. Instead, make
  parameters configurable through CLI arguments, config files, environment variables,
  or runtime queries, while providing sensible defaults.
repository: unionlabs/union
label: Configurations
language: Rust
comments_count: 3
repository_stars: 74800
---

Avoid hardcoding configuration values directly in code. Instead, make parameters configurable through CLI arguments, config files, environment variables, or runtime queries, while providing sensible defaults.

Hardcoded values reduce flexibility, make testing difficult, and require code changes for different environments. Configuration should be externalized to support different deployment contexts and operational requirements.

Examples of good practices:
- Make CLI parameters configurable: `faucet --batch-size 6000` instead of `let batch_size = 6000;`
- Fetch values from runtime sources: `voyager_client.client_info()` instead of hardcoded client types
- Use contextual defaults: `DEFAULT_DECIMALS = 6` for cosmos tokens, but allow override when needed
- Implement proper serde defaults with custom functions: `#[serde(default = "default_delay_blocks")]`

This approach improves maintainability, testability, and deployment flexibility while ensuring the system can adapt to different operational requirements without code modifications.