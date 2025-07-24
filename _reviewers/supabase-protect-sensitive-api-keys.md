---
title: Protect sensitive API keys
description: 'Never expose keys with elevated privileges (such as `service_role` or
  secret keys) in client-side code. These keys can bypass Row Level Security (RLS)
  and provide unrestricted access to your data. '
repository: supabase/supabase
label: Security
language: Other
comments_count: 4
repository_stars: 86070
---

Never expose keys with elevated privileges (such as `service_role` or secret keys) in client-side code. These keys can bypass Row Level Security (RLS) and provide unrestricted access to your data. 

Always use elevated privilege keys only in server-side environments like:
- Backend servers
- Edge Functions
- Secure CI/CD pipelines 

For client-side applications, only use the publishable or `anon` key, and ensure Row Level Security is properly configured on all tables to protect your data.

```typescript
// WRONG - Never do this in client-side code
const supabase = createClient(
  'https://your-project.supabase.co',
  'SUPABASE_SERVICE_ROLE_KEY' // Dangerous!
)

// CORRECT - Server-side code only (e.g., Edge Function)
const supabaseAdmin = createClient(
  Deno.env.get('SUPABASE_URL') ?? '',
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? '' // Secure, from environment variables
)

// CORRECT - Client-side code
const supabase = createClient(
  'https://your-project.supabase.co',
  'SUPABASE_ANON_KEY' // Safe with proper RLS policies
)
```

Additionally, ensure sensitive files containing keys (like `.env` files or `.sentryclirc`) are added to `.gitignore` to prevent accidental exposure through version control.