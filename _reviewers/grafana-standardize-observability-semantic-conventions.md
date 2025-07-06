---
title: Standardize observability semantic conventions
description: When implementing observability features (logs, metrics, traces), use
  consistent semantic conventions to ensure data can be correlated and analyzed efficiently
  across the entire system.
repository: grafana/grafana
label: Observability
language: Go
comments_count: 5
repository_stars: 68825
---

When implementing observability features (logs, metrics, traces), use consistent semantic conventions to ensure data can be correlated and analyzed efficiently across the entire system.

1. **Define core observability attributes in foundational packages** that can be imported by other components. This creates a single source of truth for naming conventions.

2. **Use semantic conventions for all observability signals** including logs, metrics, and traces:

   ```go
   // Instead of manually adding attributes with varying names:
   reqContext.Logger = reqContext.Logger.New("userId", reqContext.UserID, "orgId", reqContext.OrgID, "uname", reqContext.Login)
   
   // Use standardized attribute helpers:
   reqContext.Logger = reqContext.Logger.New(log.Attributes(
     o11ysemconv.UserID.LogKV(reqContext.UserID),
     o11ysemconv.OrgID.LogKV(reqContext.OrgID),
     o11ysemconv.Username.LogKV(reqContext.Login),
   ))
   ```

3. **Create consistent naming conventions for metrics** that reflect their purpose rather than implementation details. For example, use `remote_alertmanager_syncs_total` instead of `remote_secondary_forked_alertmanager_syncs_total`.

4. **Use centralized metrics registration** to prevent duplicate registrations:

   ```go
   // Instead of:
   prometheus.NewRegistry()
   // or
   prometheus.DefaultRegisterer
   
   // Use the provided utility:
   metrics.ProvideRegisterer()
   ```

Following these conventions ensures that observability data remains consistent and queryable across the entire system, making it easier to correlate information during debugging and analysis.