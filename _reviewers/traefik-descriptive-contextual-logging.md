---
title: descriptive contextual logging
description: Log messages should be descriptive, contextual, and provide actionable
  information. Include relevant context such as service names, configuration details,
  or affected components. When logging errors or warnings, explain what happened,
  why it matters, and what action is being taken or should be taken.
repository: traefik/traefik
label: Logging
language: Go
comments_count: 3
repository_stars: 55772
---

Log messages should be descriptive, contextual, and provide actionable information. Include relevant context such as service names, configuration details, or affected components. When logging errors or warnings, explain what happened, why it matters, and what action is being taken or should be taken.

Examples of improvements:
- Instead of: `logger.Error().Msg("Health check interval smaller than zero")`
- Use: `logger.Error().Msg("Health check interval smaller than zero, default value will be used instead.")`

- Add contextual loggers that include service-specific information rather than generic loggers
- Include warning logs when important features or configurations are used that users should be aware of

This approach helps with debugging, monitoring, and provides users with clear understanding of system behavior and any corrective actions being taken.