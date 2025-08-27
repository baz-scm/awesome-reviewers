---
title: Implement simulation testing
description: When developing complex systems like schedulers or resource managers,
  create simulation-based testing frameworks to validate functionality in scenarios
  that cannot be easily reproduced in development environments. This approach enables
  testing of hardware configurations you don't have access to (GPU/NPU nodes), large-scale
  cluster behaviors, and parameter...
repository: volcano-sh/volcano
label: Testing
language: Markdown
comments_count: 2
repository_stars: 4899
---

When developing complex systems like schedulers or resource managers, create simulation-based testing frameworks to validate functionality in scenarios that cannot be easily reproduced in development environments. This approach enables testing of hardware configurations you don't have access to (GPU/NPU nodes), large-scale cluster behaviors, and parameter changes before production deployment.

Simulation testing should provide visibility into system decision-making processes and support regression testing. For example, when testing a scheduler simulator, ensure it can show "how many nodes are there, which nodes are filtered for what reason, and how is each node scored" to enable thorough validation of scheduling logic.

Consider implementing simulation frameworks that:
- Allow testing with various node configurations (e.g., nodes.csv with gpu_allocatable fields)
- Support performance testing at different scales
- Enable debugging of scenarios unavailable in your development environment
- Provide comprehensive visibility into system behavior for validation

This testing approach is particularly valuable for validating the impact of configuration changes, such as "after change the mostrequested.weight, if the average wait time of big task is shorter than before."