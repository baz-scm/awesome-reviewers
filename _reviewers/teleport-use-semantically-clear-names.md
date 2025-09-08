---
title: Use semantically clear names
description: Choose names that clearly convey their purpose, scope, and meaning to
  reduce ambiguity and improve code maintainability. Avoid generic or potentially
  confusing terms when more specific alternatives exist.
repository: gravitational/teleport
label: Naming Conventions
language: Other
comments_count: 3
repository_stars: 19109
---

Choose names that clearly convey their purpose, scope, and meaning to reduce ambiguity and improve code maintainability. Avoid generic or potentially confusing terms when more specific alternatives exist.

Key principles:
- Replace ambiguous terms with more specific ones that accurately reflect the item's role
- Consider the broader context where the name will be used
- Use industry-standard terminology when available
- Add qualifying words to distinguish between similar concepts

Examples:
```protobuf
// Instead of generic 'role' which could mean many things
string role = 4;

// Use specific 'system_role' to clarify the type of role
string system_role = 4;
```

```protobuf
// Instead of 'node_name' which implies SSH nodes only
string node_name = 3;

// Use 'friendly_name' or 'host_name' to reflect broader applicability
string friendly_name = 3;
```

```markdown
// Instead of "App to App" which is less common
title: App to App mTLS

// Use "Service to Service" which aligns with industry terminology
title: Service to Service mTLS
```

This practice prevents confusion during code reviews, reduces onboarding time for new developers, and makes the codebase more self-documenting.