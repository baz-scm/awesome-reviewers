---
title: "Document configuration sources"
description: "When providing configuration instructions, document the exact location and method to obtain required values. Include specific paths, URLs, or UI navigation steps needed to find configuration settings."
repository: "vercel/next.js"
label: "Configurations"
language: "JSON"
comments_count: 2
repository_stars: 133000
---

When providing configuration instructions, document the exact location and method to obtain required values. Include specific paths, URLs, or UI navigation steps needed to find configuration settings. For tool-specific configurations, explain the reasoning behind non-standard settings.

Examples:
```
# Good - Clear and specific
# Update these with your Supabase details from the Connect modal via your project's project header
# https://supabase.com/dashboard/project/_?showConnect=true

# Good - Explains non-standard configuration
# Uses --watch=always instead of --watch because Turborepo doesn't wire stdin correctly
"tw-watch": "pnpm tw-build --watch=always"

# Bad - Vague and potentially outdated
# Update these with your Supabase details from your project settings
```

Including precise configuration source information reduces setup time, prevents errors, and ensures developers can efficiently update configuration values when needed.