---
title: Documentation completeness standards
description: 'Ensure all documentation meets completeness and formatting standards.
  This includes: (1) Adding language specifications to all fenced code blocks to satisfy
  linting requirements, (2) Including deprecation notes with clear migration guidance
  when removing or replacing features, and (3) Following established documentation
  patterns and embedding guidelines.'
repository: ClickHouse/ClickHouse
label: Documentation
language: Markdown
comments_count: 3
repository_stars: 42425
---

Ensure all documentation meets completeness and formatting standards. This includes: (1) Adding language specifications to all fenced code blocks to satisfy linting requirements, (2) Including deprecation notes with clear migration guidance when removing or replacing features, and (3) Following established documentation patterns and embedding guidelines.

For code blocks, always specify the language:
```sql
DESC format(JSONEachRow, '{"arr" : [42, "hello", [1, 2, 3]]}');
```

For deprecated features, provide clear migration paths:
```
system.latency_log was deprecated after version 25.x, instead system.histogram_metrics should be used
```

Consider embedding documentation directly in code when appropriate, as this keeps documentation close to implementation and reduces maintenance overhead.