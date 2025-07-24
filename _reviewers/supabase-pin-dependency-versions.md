---
title: Pin dependency versions
description: Always specify exact versions for dependencies in your configuration
  files and import statements to ensure consistent behavior across different environments.
  Unpinned dependencies can lead to unexpected breaking changes when packages are
  automatically updated to newer versions.
repository: supabase/supabase
label: Configurations
language: Other
comments_count: 4
repository_stars: 86070
---

Always specify exact versions for dependencies in your configuration files and import statements to ensure consistent behavior across different environments. Unpinned dependencies can lead to unexpected breaking changes when packages are automatically updated to newer versions.

For npm/JavaScript dependencies:
```json
{
  "dependencies": {
    "elevenlabs": "1.0.5",
    "@supabase/supabase-js": "2.38.4"
  }
}
```

For imports in Deno/Edge Functions:
```ts
import { ElevenLabsClient } from 'npm:elevenlabs@1.0.5';
import { createClient } from 'jsr:@supabase/supabase-js@2.38.4';
```

For Docker/container configurations:
```dockerfile
FROM node:20.9.0-alpine
```

This practice ensures reproducible builds, predictable behavior across development, testing, and production environments, and makes debugging easier by eliminating version inconsistencies as a potential source of problems.