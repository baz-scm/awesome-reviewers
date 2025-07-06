---
title: Document complete data flows
description: 'When documenting database systems, ensure all documentation includes
  complete end-to-end data flows. Both diagrams and textual descriptions should clearly
  indicate:'
repository: influxdata/influxdb
label: Database
language: Markdown
comments_count: 3
repository_stars: 30268
---

When documenting database systems, ensure all documentation includes complete end-to-end data flows. Both diagrams and textual descriptions should clearly indicate:

1. Where and how user requests enter the system
2. The complete path data takes through system components
3. How responses/confirmations are returned to clients
4. Precise timing and conditions for internal processes

For diagrams:
- Include entry points for user requests with clear directional arrows
- Link diagram components to numbered steps in textual descriptions
- Show all components involved in request processing

For technical descriptions:
- Include client notification mechanisms (like the oneshot channel that gets called back after flush operations)
- Provide accurate details about internal timing conditions (like exactly when WAL periods trigger snapshots)
- Clarify edge cases and exceptions to normal flows

Example improvement:
```
// Before: Incomplete diagram missing user entry point
┌────────────┐           ┌────────────┐
│flush buffer│──────────►│ wal buffer │
└────────────┘           └────────────┘

// After: Complete diagram showing user entry point and process flow
    User Write
        │
        ▼
┌────────────┐           ┌────────────┐
│flush buffer│──────────►│ wal buffer │ (Step 1: Buffer incoming writes)
└────────────┘           └────────────┘
                              │
                              ▼
                        (Step 2: Flush to disk)
```

Complete documentation helps new team members understand the system and makes debugging easier during incidents.