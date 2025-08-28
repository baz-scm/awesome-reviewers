---
title: Remove unnecessary configurations
description: Configuration files should only include options that are supported in
  production and work out of the box. Remove configuration fields that are unsupported
  in production environments, comment out configurations that require external provisioning,
  and maintain consistency across templates by removing redundant or debugging-specific
  settings.
repository: cloudflare/workers-sdk
label: Configurations
language: Other
comments_count: 3
repository_stars: 3379
---

Configuration files should only include options that are supported in production and work out of the box. Remove configuration fields that are unsupported in production environments, comment out configurations that require external provisioning, and maintain consistency across templates by removing redundant or debugging-specific settings.

Key principles:
- Remove production-unsupported options (like worker loader `id` fields)
- Comment out configurations requiring external setup (like R2 buckets) to prevent broken out-of-box experiences  
- Remove debugging/development-specific settings for template consistency (like `minify: true`)

Example from wrangler.jsonc:
```jsonc
{
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2024-09-26",
  // Remove unsupported production options
  // "unsafe": {
  //   "bindings": [
  //     {
  //       "name": "LOADER", 
  //       "type": "worker-loader"
  //       // "id": "random-id" <- Remove this
  //     }
  //   ]
  // },
  // Comment out configs requiring external provisioning
  // "r2_buckets": [
  //   {
  //     "binding": "CACHE_BUCKET",
  //     "bucket_name": "<BUCKET_NAME>"
  //   }
  // ]
}
```

This ensures templates work immediately after creation and don't include configurations that will fail in production deployments.