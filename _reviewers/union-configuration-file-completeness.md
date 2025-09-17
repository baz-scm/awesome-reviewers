---
title: Configuration file completeness
description: Ensure all configuration files contain required fields, maintain proper
  structure, and follow consistent formatting standards. Configuration files should
  be complete with all mandatory nodes present, properly sorted for consistency, and
  preserve critical values that shouldn't be auto-updated.
repository: unionlabs/union
label: Configurations
language: Json
comments_count: 4
repository_stars: 74800
---

Ensure all configuration files contain required fields, maintain proper structure, and follow consistent formatting standards. Configuration files should be complete with all mandatory nodes present, properly sorted for consistency, and preserve critical values that shouldn't be auto-updated.

Key practices:
- Validate that all required configuration nodes are present (e.g., chain_id, ibc_interface, channels)
- Maintain consistent JSON formatting using tools like `jq . config.json -S | sponge config.json`
- Categorize dependencies correctly (devDependencies vs dependencies in package.json)
- Preserve static configuration values that shouldn't change automatically (like deployment heights)

Example of proper structure validation:
```json
{
  "deployments": {
    "chain_id": "required-value",
    "ibc_interface": "required-interface", 
    "channels": [1, 2, 3],
    "core": {
      "address": "0x...",
      "height": 22242649  // should not auto-update
    }
  }
}
```

This prevents runtime errors, ensures environment consistency, and maintains configuration integrity across deployments.