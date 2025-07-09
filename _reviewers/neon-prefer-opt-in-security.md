---
title: Prefer opt-in security
description: When implementing security features that modify data presentation or
  alter normal data access patterns (like anonymization, masking, or redaction), design
  them to be explicitly enabled by users rather than activated by default. Default-enabled
  data transformation creates security and usability concerns as users may not expect
  or desire their data to be...
repository: neondatabase/neon
label: Security
language: Dockerfile
comments_count: 1
repository_stars: 19015
---

When implementing security features that modify data presentation or alter normal data access patterns (like anonymization, masking, or redaction), design them to be explicitly enabled by users rather than activated by default. Default-enabled data transformation creates security and usability concerns as users may not expect or desire their data to be modified.

For example, instead of:
```
# Adding anonymization library to default preloaded libraries
COPY --from=pg-anon-pg-build /usr/local/pgsql/ /usr/local/pgsql/
# Configuration that auto-enables the feature
shared_preload_libraries = '...,anon'
```

Prefer:
```
# Make the library available but not preloaded by default
COPY --from=pg-anon-pg-build /usr/local/pgsql/ /usr/local/pgsql/
# Provide documentation or helper functions to enable when needed
CREATE OR REPLACE FUNCTION enable_data_masking() 
RETURNS VOID AS $$
BEGIN
  PERFORM set_config('session_preload_libraries', 
                    current_setting('session_preload_libraries') || ',anon', 
                    false);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```