---
title: Minimize memory allocations
description: Reduce garbage collection pressure and improve application performance
  by avoiding unnecessary memory allocations. This significantly impacts overall system
  responsiveness, especially for high-throughput services.
repository: Azure/azure-sdk-for-net
label: Performance Optimization
language: C#
comments_count: 6
repository_stars: 5809
---

Reduce garbage collection pressure and improve application performance by avoiding unnecessary memory allocations. This significantly impacts overall system responsiveness, especially for high-throughput services.

Key practices to follow:
1. **Use shared buffers and specialized APIs** - Prefer operations that leverage pre-allocated memory:
   ```csharp
   // Instead of this (creates allocations):
   var binaryData = ModelReaderWriter.Write(model);
   return RequestContent.Create(binaryData);
   
   // Use this (leverages shared buffers):
   return BinaryContent.Create(model); // Uses UnsafeBufferSequence internally
   ```

2. **Work directly with Spans** - Avoid copying when operating on memory regions:
   ```csharp
   // Instead of this (allocates new array):
   json.WriteString("certificate", Convert.ToBase64String(data.ToArray()));
   
   // Use this (avoids allocation):
   json.WriteString("certificate", Convert.ToBase64String(data.Span));
   ```

3. **Cache infrequently-changing data** - Balance freshness with performance:
   ```csharp
   // Cache agent tools to avoid API calls on every request
   if (_agentTools is null)
   {
       PersistentAgent agent = await _client.Administration.GetAgentAsync(_agentId);
       _agentTools = agent.Tools;
   }
   ```

4. **Use streaming APIs for large data** - Process data incrementally instead of loading everything into memory:
   ```csharp
   // Instead of loading the whole stream:
   var allProfile = BinaryData.FromStream(stream).ToObjectFromJson<Dictionary<string, Dictionary<string, object>>>();
   
   // Use streaming deserialization:
   var allProfile = await JsonSerializer.DeserializeAsync<Dictionary<string, Dictionary<string, JsonElement>>>(stream, options);
   ```

5. **Reuse objects** for repeated operations rather than creating new instances each time.

These optimizations are particularly important in high-throughput scenarios where allocation pressure can cause frequent garbage collections, leading to performance degradation.
