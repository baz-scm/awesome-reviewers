---
title: Use semantic naming
description: Choose names that clearly communicate purpose and align with established
  domain terminology. Prioritize semantic clarity over brevity, and ensure consistency
  with the codebase's vocabulary.
repository: mastodon/mastodon
label: Naming Conventions
language: Other
comments_count: 5
repository_stars: 48691
---

Choose names that clearly communicate purpose and align with established domain terminology. Prioritize semantic clarity over brevity, and ensure consistency with the codebase's vocabulary.

Key principles:
- Use domain-consistent terminology (e.g., `MAX_STATUS_CHARS` instead of `MAX_TOOT_CHARS` when "status" is the established term in code)
- Name components based on their actual scope and purpose (e.g., `moderation_notes` instead of `report_notes` when used across multiple contexts)
- Extract complex logic into descriptively named methods that communicate their intent
- Choose user-appropriate terminology in UI contexts (e.g., "Filtered" instead of technical terms like "NOOP")

Example of good semantic naming:
```ruby
# Instead of inline complex logic:
if @report.account.local? && !@statuses.empty? && (@report.account.user.settings['web.expand_content_warnings'] || @report.account.user.settings['web.display_media'] == 'show_all')

# Extract to semantically named method:
if @report.account.local? && !@statuses.empty? && @report.account.user.all_content_visible?

# Method clearly communicates its purpose:
def all_content_visible?
  settings['web.expand_content_warnings'] || settings['web.display_media'] == 'show_all'
end
```

This approach reduces cognitive load, improves code maintainability, and makes the codebase more accessible to new developers.