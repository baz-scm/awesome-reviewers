---
title: Sanitize all inputs
description: 'Properly sanitize or escape all user-provided inputs before using them
  in sensitive contexts to prevent injection attacks. This applies to multiple contexts:'
repository: elie222/inbox-zero
label: Security
language: TypeScript
comments_count: 11
repository_stars: 8267
---

Properly sanitize or escape all user-provided inputs before using them in sensitive contexts to prevent injection attacks. This applies to multiple contexts:

1. **SQL/OData queries**: Use parameterized queries or properly escape special characters:
```diff
-request = request.filter(`contains(subject, '${query}')`);
+const escapedQuery = query.replace(/'/g, "''");
+request = request.filter(`contains(subject, '${escapedQuery}')`);
```

2. **HTML content**: Use a library like DOMPurify to sanitize HTML before rendering:
```diff
-return `<div dir="ltr">${latestReplyHtml}</div>`;
+return DOMPurify.sanitize(`<div dir="ltr">${latestReplyHtml}</div>`);
```

3. **XML construction**: Escape special characters in XML:
```diff
-<rule_name>${rule.name}</rule_name>
+<rule_name>${escape(rule.name)}</rule_name>
```

4. **AI prompts**: Sanitize inputs before inclusion in prompts:
```diff
-${user.about ? `<user_info>${user.about}</user_info>` : ""}
+${user.about ? `<user_info>${sanitizeText(user.about)}</user_info>` : ""}
```

Input sanitization is your first line of defense against injection vulnerabilities and should be applied consistently throughout your codebase.