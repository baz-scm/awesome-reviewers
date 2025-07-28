---
title: Consistent documentation language
description: 'Maintain consistency in wording, formatting, and specificity across
  all documentation strings to improve readability and translation quality.


  Key practices:'
repository: home-assistant/core
label: Documentation
language: Json
comments_count: 4
repository_stars: 80450
---

Maintain consistency in wording, formatting, and specificity across all documentation strings to improve readability and translation quality.

Key practices:
- Use consistent phrasing patterns for similar concepts (e.g., "A [template]... to compose the payload to be published at the xyz topic")
- Avoid unnecessary words like "Select" in descriptions - prefer direct statements ("The instance where..." vs "Select the instance where...")
- Use proper capitalization and avoid ALL CAPS for better translatability
- Be specific in descriptions rather than generic (e.g., "to extract the current humidity value" vs "to extract the payload for the current humidity topic")
- Proofread for typos that can confuse users and translators

Example of consistent template description:
```json
{
  "fan_mode_command_template": "A [template](https://example.com) to compose the payload to be published at the fan mode command topic.",
  "power_command_template": "A [template](https://example.com) to compose the payload to be published at the power command topic."
}
```

This ensures documentation is professional, clear, and maintainable across the entire codebase while supporting internationalization efforts.