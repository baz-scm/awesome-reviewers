---
title: consistent route nesting
description: Maintain consistent URL patterns and nesting structures across similar
  API endpoints to ensure predictable and intuitive interfaces. When designing routes
  for related resources, apply the same nesting strategy throughout the application
  rather than mixing top-level and nested approaches.
repository: mastodon/mastodon
label: API
language: Other
comments_count: 2
repository_stars: 48691
---

Maintain consistent URL patterns and nesting structures across similar API endpoints to ensure predictable and intuitive interfaces. When designing routes for related resources, apply the same nesting strategy throughout the application rather than mixing top-level and nested approaches.

In the example, instance notes were nested under instances (`/admin/instances/:instance_id/notes/:id`) while similar resources like account moderation notes and report notes used top-level routes (`/admin/account_moderation_notes/:id`, `/admin/report_notes/:id`). This inconsistency makes the API harder to understand and use.

Choose one approach and apply it consistently:
```ruby
# Consistent nested approach
/admin/instances/:instance_id/notes/:id
/admin/accounts/:account_id/moderation_notes/:id  
/admin/reports/:report_id/notes/:id

# OR consistent top-level approach
/admin/instance_notes/:id
/admin/account_moderation_notes/:id
/admin/report_notes/:id
```

Additionally, ensure resources are properly addressable by providing unique identifiers (like DOM IDs) that allow direct linking to specific items, enabling permalink functionality for better user experience and API usability.