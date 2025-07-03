---
title: Write deterministic tests
description: 'Tests should be deterministic, reliable, and isolated from external
  dependencies to ensure consistent results across environments. To achieve this:


  1. **Avoid direct network calls** that can introduce flakiness and slow down tests.
  Instead:'
repository: Azure/azure-sdk-for-net
label: Testing
language: C#
comments_count: 4
repository_stars: 5809
---

Tests should be deterministic, reliable, and isolated from external dependencies to ensure consistent results across environments. To achieve this:

1. **Avoid direct network calls** that can introduce flakiness and slow down tests. Instead:
   ```csharp
   // Don't do this in tests:
   message.Request.Uri.Reset(new Uri("https://www.example.com"));
   
   // Use one of these approaches instead:
   // Option 1: Mock the transport
   var mockTransport = new MockHttpClientTransport();
   var options = new ClientOptions { Transport = mockTransport };
   
   // Option 2: Use TestServer
   var server = new TestServer();
   var client = new Client(server.BaseAddress, options);
   ```

2. **Avoid using reflection in tests** as it creates brittle code that breaks when implementation details change. Instead, expose test-friendly mechanisms:
   ```csharp
   // Avoid this:
   var field = typeof(ServiceBusRetryPolicy).GetField("_serverBusyState", 
       System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);
   field.SetValue(policy, 1);
   
   // Better approach: Add internal/protected methods for testing
   // In production code:
   internal void SetServerBusyStateForTesting(bool isBusy) { _serverBusyState = isBusy ? 1 : 0; }
   ```

3. **Use proper content comparison** for complex objects instead of reference equality:
   ```csharp
   // Incorrect:
   Assert.AreEqual(sourceStream, destinationStream); // Checks reference equality
   
   // Correct:
   byte[] sourceBytes = sourceStream.ReadAllBytes();
   byte[] destinationBytes = destinationStream.ReadAllBytes();
   Assert.AreEqual(sourceBytes.Length, destinationBytes.Length);
   CollectionAssert.AreEqual(sourceBytes, destinationBytes);
   ```

4. **Replace fixed delays with polling** to avoid flaky tests and unnecessary wait times:
   ```csharp
   // Avoid:
   await Task.Delay(TimeSpan.FromSeconds(5));
   
   // Better approach:
   await WaitForConditionAsync(
       async () => await client.GetStatus() == ExpectedStatus,
       TimeSpan.FromSeconds(10),  // Timeout
       TimeSpan.FromMilliseconds(500) // Polling interval
   );
   ```

These practices ensure tests remain stable across environments and over time, reducing maintenance costs and improving developer productivity.
