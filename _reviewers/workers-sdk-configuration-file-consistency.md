---
title: Configuration file consistency
description: Ensure consistent patterns for configuration files, proper exclusion
  of development artifacts, and clear environment-specific handling across projects.
repository: cloudflare/workers-sdk
label: Configurations
language: Markdown
comments_count: 5
repository_stars: 3379
---

Ensure consistent patterns for configuration files, proper exclusion of development artifacts, and clear environment-specific handling across projects.

**Key practices:**

1. **Use proper .gitignore patterns** - Include wildcards for development files:
```gitignore
.wrangler
.dev.vars*
```

2. **Maintain configuration format consistency** - When migrating between formats (e.g., wrangler.toml to wrangler.json), ensure all templates and documentation are updated consistently to avoid breaking changes.

3. **Handle environment-specific configurations clearly** - Use environment variables like `CLOUDFLARE_ENV` to select configurations at build/dev time:
```toml
# wrangler.toml
name = "my-worker"
vars = { MY_VAR = "Top-level var" }

[env.production]
vars = { MY_VAR = "Production var" }
```

4. **Ensure all project types include necessary exclusions** - Both worker templates and full-stack framework templates should include wrangler-related files in .gitignore to prevent committing temporary build artifacts and sensitive development files.

This prevents configuration drift, avoids committing sensitive development files, and ensures consistent behavior across different environments and project types.