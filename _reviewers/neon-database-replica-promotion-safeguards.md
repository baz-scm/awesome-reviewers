---
title: Database replica promotion safeguards
description: 'When implementing database replica promotion logic, avoid temporary
  workarounds that bypass validation checks. Instead, design a comprehensive approach
  that maintains data integrity throughout the promotion process. Consider these best
  practices:'
repository: neondatabase/neon
label: Database
language: Other
comments_count: 2
repository_stars: 19015
---

When implementing database replica promotion logic, avoid temporary workarounds that bypass validation checks. Instead, design a comprehensive approach that maintains data integrity throughout the promotion process. Consider these best practices:

1. Carefully evaluate whether streams need to be reestablished when a replica is promoted to primary
2. Explicitly handle timeline management during promotion events
3. Test promotion scenarios thoroughly to identify edge cases

For example, instead of using flags to bypass validation checks:

```
// Avoid this approach
if (SkipXLogPageHeader(wp, wp->propTermStartLsn) != wp->api.get_redo_start_lsn(wp) && !replica_promote)
{
    // Validation logic here
}
```

Consider implementing proper state transition handling:

```
// Better approach
if (isReplicaPromotion) {
    // Handle LSN alignment explicitly for promotion case
    SetRedoStartLsn(wp, SkipXLogPageHeader(wp, wp->propTermStartLsn));
} else if (SkipXLogPageHeader(wp, wp->propTermStartLsn) != wp->api.get_redo_start_lsn(wp)) {
    // Normal validation logic for non-promotion case
}
```

This ensures proper state management during replica promotion while maintaining the integrity of validation checks for normal operations.