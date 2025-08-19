---
title: validate schema decisions
description: When reviewing database schema changes or data structure modifications,
  ensure that field inclusion/exclusion decisions are explicitly justified and documented.
  Question ambiguous schema choices and require clear rationale for data organization
  patterns.
repository: PostHog/posthog
label: Database
language: Other
comments_count: 2
repository_stars: 28460
---

When reviewing database schema changes or data structure modifications, ensure that field inclusion/exclusion decisions are explicitly justified and documented. Question ambiguous schema choices and require clear rationale for data organization patterns.

Schema decisions should address:
- Why specific fields are included or omitted (e.g., "Do we need team_id in addition to person_id and event_name?")
- How the chosen structure supports expected query patterns
- Whether data access methods are intuitive for developers

Example from schema design:
```sql
-- Migration: Create person event occurrences table
-- Question: Is team_id necessary alongside person_id and event_name?
CREATE TABLE IF NOT EXISTS person_event_occurrences (
    team_id INT,  -- Rationale needed: Does this enable required queries?
    person_id TEXT,
    event_name TEXT
);
```

When data property references seem unclear or confusing (like choosing between `$groups: { key: value }` vs `$group_0`), document the reasoning behind the chosen approach and consider developer experience in accessing the data.