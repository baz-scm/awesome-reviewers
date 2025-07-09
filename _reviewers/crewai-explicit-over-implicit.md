---
title: Explicit over implicit
description: Always explicitly configure important system components rather than relying
  on implicit defaults or environment variables. Document required configuration combinations
  and version requirements clearly to prevent subtle errors.
repository: crewaiinc/crewai
label: Configurations
language: Other
comments_count: 3
repository_stars: 33945
---

Always explicitly configure important system components rather than relying on implicit defaults or environment variables. Document required configuration combinations and version requirements clearly to prevent subtle errors.

For example:
- When configuring storage backends like PostgreSQL, explicitly create and pass the configuration objects:
```python
# Explicit PostgreSQL configuration
postgres_storage = LTMPostgresStorage(
    connection_string="postgresql://username:password@hostname:5432/database"
)
long_term_memory = LongTermMemory(storage=postgres_storage)

# Configure both required components for automatic memory saving
crew = Crew(
    agents=[...],
    tasks=[...],
    memory=True,
    long_term_memory=long_term_memory,
    entity_memory=EntityMemory()
)
```

- For version requirements, specify exact minimum versions (e.g., Python >=3.10) rather than recommendations when functionality depends on it

- When adding configuration flags, use consistent, explicit naming that clearly communicates scope and function (like `-kn` for all knowledge and `-akn` for agent-specific knowledge)