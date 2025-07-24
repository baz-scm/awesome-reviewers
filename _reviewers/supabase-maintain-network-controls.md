---
title: Maintain network controls
description: Create maintainable and clearly documented network access controls. Instead
  of hardcoding network restrictions, use dedicated tables that can be updated without
  code changes. Always document networking concepts with plain language explanations
  for developers unfamiliar with networking terminology.
repository: supabase/supabase
label: Networking
language: Other
comments_count: 4
repository_stars: 86070
---

Create maintainable and clearly documented network access controls. Instead of hardcoding network restrictions, use dedicated tables that can be updated without code changes. Always document networking concepts with plain language explanations for developers unfamiliar with networking terminology.

For IP filtering:
```sql
-- Create a dedicated table for IP blocklist
CREATE TABLE private.auth_ip_blocklist (
  blocked_range cidr, 
  reason text,
  created_at timestamp DEFAULT now()
);

-- Use the table in your filtering logic
CREATE OR REPLACE FUNCTION public.check_ip_access(client_ip inet)
RETURNS boolean AS $$
BEGIN
  RETURN NOT EXISTS (
    SELECT 1 FROM private.auth_ip_blocklist 
    WHERE client_ip <<= blocked_range
  );
END;
$$ LANGUAGE plpgsql;
```

When implementing WebSocket authorization, clearly indicate when private channels are required:

```ts
// Set up a private channel listener with proper authorization
const channel = supabase.channel('topic:' + recordId, {
  config: { 
    broadcast: { 
      self: true 
    },
    private: true  // Required for realtime.broadcast_changes
  }
})
```

Always include explanations of networking terms in documentation or code comments, especially for concepts like CIDR notation, WebSocket protocols, or authentication mechanisms.