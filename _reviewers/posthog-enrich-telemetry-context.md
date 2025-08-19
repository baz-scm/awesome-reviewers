---
title: Enrich telemetry context
description: Always include relevant contextual metadata when capturing telemetry
  data (events, exceptions, logs, metrics) to improve debugging and operational visibility.
  This includes user information, team ownership, product areas, IP addresses, user
  agents, geographic data, and other relevant context that helps with troubleshooting
  and error assignment.
repository: PostHog/posthog
label: Observability
language: Python
comments_count: 2
repository_stars: 28460
---

Always include relevant contextual metadata when capturing telemetry data (events, exceptions, logs, metrics) to improve debugging and operational visibility. This includes user information, team ownership, product areas, IP addresses, user agents, geographic data, and other relevant context that helps with troubleshooting and error assignment.

When capturing exceptions, include contextual information like:
```python
capture_exception(
    e,
    {
        "project_id": project_id,
        "user_id": request.user.id if request.user else None,
        "user_distinct_id": request.user.distinct_id if request.user else None,
        "ai_product": "wizard",
        "team": "growth"  # Makes it easier for auto-assignment in error tracker
    }
)
```

When logging events or actions, include debugging properties:
```python
report_user_action(user=user, event="login notification sent", properties={
    "ip_address": ip_address,
    "user_agent": short_user_agent,
    "location": location,
    "login_time": login_time_str
})
```

Rich contextual data transforms raw telemetry into actionable insights, enabling faster debugging, better error routing, and more effective monitoring.