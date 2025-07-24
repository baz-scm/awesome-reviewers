---
title: Consistent placeholder conventions
description: Ensure all placeholders in localization files follow consistent naming
  conventions to prevent runtime errors and text leakage in the UI. This applies to
  both sprintf-style placeholders (`%s`) and template variables (`{% raw %}{{name}}{% endraw %}`).
repository: appwrite/appwrite
label: Naming Conventions
language: Json
comments_count: 7
repository_stars: 51959
---

Ensure all placeholders in localization files follow consistent naming conventions to prevent runtime errors and text leakage in the UI. This applies to both sprintf-style placeholders (`%s`) and template variables (`{% raw %}{{name}}{% endraw %}`).

Common issues to watch for:
1. **Correct sprintf order**: Use `%s` not `s%`
   {% raw %}
   ```diff
   -"emails.invitation.subject": "Invitació a l'equip %s a s%",
   +"emails.invitation.subject": "Invitació a l'equip %s a %s",
   ```
   {% endraw %}


Placeholder errors are particularly problematic because they can:
- Break runtime string substitution
- Cause literal placeholder text to appear in the UI
- Lead to crashes in formatting functions
- Create inconsistent user experiences across languages
