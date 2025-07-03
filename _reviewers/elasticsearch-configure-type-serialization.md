---
title: Configure type serialization
description: When working with databases that exchange data with other systems, ensure
  proper serialization and deserialization of data types like UUIDs, dates, or complex
  objects. System-specific representation differences can lead to data corruption,
  query failures, or incorrect results.
repository: elastic/elasticsearch
label: Database
language: Markdown
comments_count: 4
repository_stars: 73104
---

When working with databases that exchange data with other systems, ensure proper serialization and deserialization of data types like UUIDs, dates, or complex objects. System-specific representation differences can lead to data corruption, query failures, or incorrect results.

For example, when working with MongoDB and UUIDs:

```
# Specify UUID representation in connection string
mongodb+srv://username:password@cluster.mongodb.net/mydb?uuidRepresentation=standard

# For legacy UUID representations, use appropriate parameters:
# - C#: uuidRepresentation=csharpLegacy
# - Java: uuidRepresentation=javaLegacy
# - Python: uuidRepresentation=pythonLegacy
```

When joining data across different sources, ensure join keys have compatible data types:
- Integer types (`byte`, `short`, `integer`) can typically be joined
- Float types (`half_float`, `float`, `scaled_float`, `double`) are often interchangeable
- Date types often require exact matching or explicit conversion
- Text/string types may require specific formatting or normalization

Always document data type compatibility requirements in your schema design and provide conversion functions where needed to ensure consistent data handling across systems.
