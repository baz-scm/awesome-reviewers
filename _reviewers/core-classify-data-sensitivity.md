---
title: classify data sensitivity
description: Properly evaluate whether data contains sensitive information before
  applying security measures like redaction. Not all identifiers or structured data
  require protection - understand the nature and content of the data to make informed
  security decisions.
repository: home-assistant/core
label: Security
language: Other
comments_count: 1
repository_stars: 80450
---

Properly evaluate whether data contains sensitive information before applying security measures like redaction. Not all identifiers or structured data require protection - understand the nature and content of the data to make informed security decisions.

For example, group IDs that are random strings (like `66a810bbaa36cf27c75073afb71aeda4b6b1f9d4-422`) don't contain personal information and may not need redaction in test snapshots, while actual user credentials or personal identifiers would require protection.

```python
# Good - Understanding data nature before redaction
'groups': dict({
  'test-groupid': dict({  # Random string, not sensitive
    'name': '**REDACTED**',  # Actual group name may be sensitive
  }),
})
```

Consider the actual content and purpose of data rather than applying blanket security policies to all structured information.