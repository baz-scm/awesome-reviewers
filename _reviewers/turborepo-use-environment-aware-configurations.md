---
title: Use environment-aware configurations
description: Configure paths and system references dynamically to ensure they work
  across all environments (development, testing, production). Avoid hardcoded paths
  or environment-specific values that will break when code is packaged or deployed.
repository: vercel/turborepo
label: Configurations
language: JavaScript
comments_count: 2
repository_stars: 28115
---

Configure paths and system references dynamically to ensure they work across all environments (development, testing, production). Avoid hardcoded paths or environment-specific values that will break when code is packaged or deployed.

For file paths:
```javascript
// Avoid this:
const filePath = "../../../../../examples/basic/README.md";

// Use this instead:
const rootReadme = path.join(prompts.root, "README.md");
// Or with @turbo/workspaces:
const rootReadme = path.join(project.paths.root, "README.md");
```

For tool-specific code:
```javascript
// Avoid hardcoding for specific package managers:
data = data.replace(/\bpnpm\b/g, `${selectedPackageManager} run`);

// Make it work for all package managers:
// Transform from any package manager to the selected one
```

This approach ensures configurations remain portable across different environments and development setups, preventing unexpected failures during deployment or when sharing code with other team members.