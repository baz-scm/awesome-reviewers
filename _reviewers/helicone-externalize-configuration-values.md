---
title: Externalize configuration values
description: Avoid hardcoding deployment-specific values—such as usernames, channel
  IDs, thresholds, or other identifiers—directly in source code. Instead, define them
  as environment variables or config entries (e.g., `CLICKHOUSE_HQL_USER` instead
  of a literal `"hql_user"`, or `ALERT_BANNER_ID_DELAY_IN_QUEUE`/`FIRE_ALERT_CHANNEL`
  as env vars rather than inline...
repository: Helicone/helicone
label: Configurations
language: TypeScript
comments_count: 3
repository_stars: 6248
---

Avoid hardcoding deployment-specific values—such as usernames, channel IDs, thresholds, or other identifiers—directly in source code. Instead, define them as environment variables or config entries (e.g., `CLICKHOUSE_HQL_USER` instead of a literal `"hql_user"`, or `ALERT_BANNER_ID_DELAY_IN_QUEUE`/`FIRE_ALERT_CHANNEL` as env vars rather than inline constants). This is especially important for self-hosted or multi-environment deployments where these values must be customizable without code changes.

Additionally, when a feature depends on optional configuration (e.g., Slack webhook/channel settings), guard the code path so it skips gracefully if that configuration is not set, rather than attempting the action and failing. For example:

```ts
if (!env.SLACK_ALERT_CHANNEL) {
  return; // skip sending alert if not configured
}
await alertManager.sendSlackMessageToChannel(env.SLACK_ALERT_CHANNEL, ...);
```

This keeps configuration centralized, makes deployments portable, and prevents runtime failures when optional settings are absent.