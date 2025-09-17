---
title: maintain code consistency
description: Ensure consistent patterns, formatting, and conventions throughout the
  codebase. Inconsistencies in code style create confusion, reduce readability, and
  make maintenance more difficult.
repository: emcie-co/parlant
label: Code Style
language: Python
comments_count: 11
repository_stars: 12205
---

Ensure consistent patterns, formatting, and conventions throughout the codebase. Inconsistencies in code style create confusion, reduce readability, and make maintenance more difficult.

Key areas to maintain consistency:

**Import Organization**: Group imports consistently and separate them with blank lines:
```python
# Standard library imports
import os
from pathlib import Path

# Third-party imports  
from lagom import Container
from pytest import fixture

# Internal imports
from emcie.server.core.common import ItemNotFoundError, JSONSerializable
```

**Parameter Formatting**: Use trailing commas consistently for multi-line parameters:
```python
def create_session(
    self,
    end_user_id: EndUserId,
    client_id: str,
) -> Session:  # trailing comma enables easy additions
```

**Naming and Capitalization**: Choose one scheme and apply it consistently across similar contexts:
```python
# Consistent predicate capitalization
"The user asks about weather"  # or
"the user asks about weather"  # but not mixed
```

**Code Patterns**: When establishing a pattern (like error handling, logging format, or method signatures), apply it uniformly across the codebase. Before introducing variations, consider if the existing pattern should be updated everywhere or if the new context truly requires different handling.

Review your changes to ensure they follow the same conventions used elsewhere in the codebase. When in doubt, search for similar code patterns and match their style.