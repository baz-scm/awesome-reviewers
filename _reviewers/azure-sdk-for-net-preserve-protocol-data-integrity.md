---
title: Preserve protocol data integrity
description: When working with network protocols (like AMQP, NFS, or SMB), maintain
  the integrity of the original protocol data structures during serialization, deserialization,
  and transformation operations. Modifying protocol-specific data can lead to unintended
  changes in the service contract and unexpected behavior for clients.
repository: Azure/azure-sdk-for-net
label: Networking
language: Markdown
comments_count: 2
repository_stars: 5809
---

When working with network protocols (like AMQP, NFS, or SMB), maintain the integrity of the original protocol data structures during serialization, deserialization, and transformation operations. Modifying protocol-specific data can lead to unintended changes in the service contract and unexpected behavior for clients.

For message-based protocols:
- Avoid mutating the underlying protocol representation when converting to language-specific objects
- Perform type normalization only on your application's representation of the data, not on the protocol layer
- Document how special cases are handled when converting between protocol formats

Example from AMQP handling:
```csharp
// Incorrect: Directly modifying protocol data
amqpMessage.Properties.ContentType = normalizedContentType; // Mutates original AMQP data

// Correct: Keep protocol representation intact, normalize only in your model
EventData eventData = new EventData(amqpMessage);
eventData.ContentType = normalizedContentType; // Only the .NET projection is affected
```

For file transfer protocols:
- Clearly document how specialized elements (like symbolic links, hard links) are handled
- Ensure consistent behavior across different transfer operations
- Preserve protocol-specific properties where possible to maintain compatibility
