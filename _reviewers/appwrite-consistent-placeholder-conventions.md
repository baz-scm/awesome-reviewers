---
title: Consistent placeholder conventions
description: Ensure all placeholders in localization files follow consistent naming
  conventions to prevent runtime errors and text leakage in the UI. This applies to
  both sprintf-style placeholders (`%s`) and template variables (`{{name}}`).
repository: appwrite/appwrite
label: Naming Conventions
language: Json
comments_count: 7
repository_stars: 51959
---

Ensure all placeholders in localization files follow consistent naming conventions to prevent runtime errors and text leakage in the UI. This applies to both sprintf-style placeholders (`%s`) and template variables (`{{name}}`).

Common issues to watch for:
1. **Correct sprintf order**: Use `%s` not `s%`
   ```diff
   -"emails.invitation.subject": "Invitació a l'equip %s a s%",
   +"emails.invitation.subject": "Invitació a l'equip %s a %s",
   ```

2. **Complete template variables**: Always include both opening and closing braces
   ```diff
   -"emails.invitation.buttonText": "Accetta invito a {{team}",
   +"emails.invitation.buttonText": "Accetta invito a {{team}}",
   ```
   
3. **Proper variable name boundaries**: Don't let punctuation merge with variable names
   ```diff
   -"emails.invitation.buttonText": "Elfogadni meghívást a {{team}-re",
   +"emails.invitation.buttonText": "Elfogadni meghívást a {{team}}-re",
   ```

Placeholder errors are particularly problematic because they can:
- Break runtime string substitution
- Cause literal placeholder text to appear in the UI
- Lead to crashes in formatting functions
- Create inconsistent user experiences across languages