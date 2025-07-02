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


[
  {
    "discussion_id": "2155220117",
    "pr_number": 50534,
    "pr_file": "sdk/core/Azure.Core/Benchmarks.Nuget/PipelineScenario.cs",
    "created_at": "2025-06-18T18:14:23+00:00",
    "commented_code": "\ufeffusing System;\nusing System.Net.Http;\nusing System.Threading;\nusing System.Threading.Tasks;\nusing Azure.Core;\nusing Azure.Core.Pipeline;\n\nnamespace Benchmarks.Nuget\n{\n    public class PipelineScenario\n    {\n        public readonly HttpPipeline _pipeline;\n\n        public PipelineScenario()\n        {\n            var options = new BenchmarkClientOptions\n            {\n                Transport = new HttpClientTransport(new HttpClient())\n            };\n            _pipeline = HttpPipelineBuilder.Build(options);\n        }\n\n        public async Task<Azure.Response> SendAsync()\n        {\n            var message = _pipeline.CreateMessage();\n            message.Request.Uri.Reset(new Uri(\"https://www.example.com\"));\n            await _pipeline.SendAsync(message, CancellationToken.None);",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2155220117",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50534,
        "pr_file": "sdk/core/Azure.Core/Benchmarks.Nuget/PipelineScenario.cs",
        "discussion_id": "2155220117",
        "commented_code": "@@ -0,0 +1,33 @@\n+\ufeffusing System;\n+using System.Net.Http;\n+using System.Threading;\n+using System.Threading.Tasks;\n+using Azure.Core;\n+using Azure.Core.Pipeline;\n+\n+namespace Benchmarks.Nuget\n+{\n+    public class PipelineScenario\n+    {\n+        public readonly HttpPipeline _pipeline;\n+\n+        public PipelineScenario()\n+        {\n+            var options = new BenchmarkClientOptions\n+            {\n+                Transport = new HttpClientTransport(new HttpClient())\n+            };\n+            _pipeline = HttpPipelineBuilder.Build(options);\n+        }\n+\n+        public async Task<Azure.Response> SendAsync()\n+        {\n+            var message = _pipeline.CreateMessage();\n+            message.Request.Uri.Reset(new Uri(\"https://www.example.com\"));\n+            await _pipeline.SendAsync(message, CancellationToken.None);",
        "comment_created_at": "2025-06-18T18:14:23+00:00",
        "comment_author": "m-redding",
        "comment_body": "When you're running this, does this work with the example.com uri?\r\n\r\nYou could consider a few alternatives since we want to avoid network calls to isolate client code:\r\n- mocking the transport - it looks like PipelineBenchmark used to use a mock HTTP handler implementation https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/core/Azure.Core/perf/PipelineBenchmark.cs#L66\r\n- using a TestServer. This is an example of using a test server https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/core/System.ClientModel/tests/Pipeline/ClientPipelineFunctionalTests.cs#L40-L46\r\n- integrating with the test proxy https://github.com/Azure/azure-sdk-tools/blob/main/tools/test-proxy/Azure.Sdk.Tools.TestProxy/README.md",
        "pr_file_module": null
      },
      {
        "comment_id": "2157684780",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50534,
        "pr_file": "sdk/core/Azure.Core/Benchmarks.Nuget/PipelineScenario.cs",
        "discussion_id": "2155220117",
        "commented_code": "@@ -0,0 +1,33 @@\n+\ufeffusing System;\n+using System.Net.Http;\n+using System.Threading;\n+using System.Threading.Tasks;\n+using Azure.Core;\n+using Azure.Core.Pipeline;\n+\n+namespace Benchmarks.Nuget\n+{\n+    public class PipelineScenario\n+    {\n+        public readonly HttpPipeline _pipeline;\n+\n+        public PipelineScenario()\n+        {\n+            var options = new BenchmarkClientOptions\n+            {\n+                Transport = new HttpClientTransport(new HttpClient())\n+            };\n+            _pipeline = HttpPipelineBuilder.Build(options);\n+        }\n+\n+        public async Task<Azure.Response> SendAsync()\n+        {\n+            var message = _pipeline.CreateMessage();\n+            message.Request.Uri.Reset(new Uri(\"https://www.example.com\"));\n+            await _pipeline.SendAsync(message, CancellationToken.None);",
        "comment_created_at": "2025-06-19T21:37:22+00:00",
        "comment_author": "sa7936",
        "comment_body": "I put back the mocking of transport calls ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2124976957",
    "pr_number": 50394,
    "pr_file": "sdk/servicebus/Azure.Messaging.ServiceBus/tests/Primitives/ServiceBusRetryPolicyTests.cs",
    "created_at": "2025-06-03T21:40:01+00:00",
    "commented_code": "return null;\n            }\n        }\n\n        private class CustomServerBusyMockRetryPolicy : ServiceBusRetryPolicy\n        {\n            public const int MaxRetries = 3;\n\n            private int _retryCount = 0;\n\n            public int CalculateRetryDelayCallCount { get; private set; }\n\n            public void SetServerBusyForTest()\n            {\n                // Set the private _serverBusyState to ServerBusyState (1)\n                var field = typeof(ServiceBusRetryPolicy).GetField(\"_serverBusyState\", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2124976957",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50394,
        "pr_file": "sdk/servicebus/Azure.Messaging.ServiceBus/tests/Primitives/ServiceBusRetryPolicyTests.cs",
        "discussion_id": "2124976957",
        "commented_code": "@@ -114,5 +175,81 @@ public override TimeSpan CalculateTryTimeout(int attemptCount)\n                 return null;\n             }\n         }\n+\n+        private class CustomServerBusyMockRetryPolicy : ServiceBusRetryPolicy\n+        {\n+            public const int MaxRetries = 3;\n+\n+            private int _retryCount = 0;\n+\n+            public int CalculateRetryDelayCallCount { get; private set; }\n+\n+            public void SetServerBusyForTest()\n+            {\n+                // Set the private _serverBusyState to ServerBusyState (1)\n+                var field = typeof(ServiceBusRetryPolicy).GetField(\"_serverBusyState\", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);",
        "comment_created_at": "2025-06-03T21:40:01+00:00",
        "comment_author": "Copilot",
        "comment_body": "Consider exposing a protected setter or an internal method in ServiceBusRetryPolicy to modify the server busy state instead of using reflection in test helper classes. This will reduce brittleness in tests if the underlying field name changes.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2112263732",
    "pr_number": 50304,
    "pr_file": "sdk/storage/Azure.Storage.DataMovement.Files.Shares/tests/ShareFileStartTransferDownloadTests.cs",
    "created_at": "2025-05-28T16:04:05+00:00",
    "commented_code": "using Stream sourceStream = await hardlinkClient.OpenReadAsync();\n            using Stream destinationStream = File.OpenRead(destinationResource.Uri.LocalPath);\n            Assert.AreEqual(sourceStream.Length, destinationStream.Length);\n            Assert.AreEqual(sourceStream, destinationStream);",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2112263732",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50304,
        "pr_file": "sdk/storage/Azure.Storage.DataMovement.Files.Shares/tests/ShareFileStartTransferDownloadTests.cs",
        "discussion_id": "2112263732",
        "commented_code": "@@ -132,6 +132,7 @@ await TestTransferWithTimeout.WaitForCompletionAsync(\n             using Stream sourceStream = await hardlinkClient.OpenReadAsync();\n             using Stream destinationStream = File.OpenRead(destinationResource.Uri.LocalPath);\n             Assert.AreEqual(sourceStream.Length, destinationStream.Length);\n+            Assert.AreEqual(sourceStream, destinationStream);",
        "comment_created_at": "2025-05-28T16:04:05+00:00",
        "comment_author": "Copilot",
        "comment_body": "Comparing two Stream objects with Assert.AreEqual checks reference equality rather than content. Consider reading both streams into byte arrays and comparing their sequences, or using a helper method to verify that the contents match.\n```suggestion\n            byte[] sourceBytes;\n            byte[] destinationBytes;\n\n            using (MemoryStream sourceMemoryStream = new MemoryStream())\n            {\n                await sourceStream.CopyToAsync(sourceMemoryStream);\n                sourceBytes = sourceMemoryStream.ToArray();\n            }\n\n            using (MemoryStream destinationMemoryStream = new MemoryStream())\n            {\n                await destinationStream.CopyToAsync(destinationMemoryStream);\n                destinationBytes = destinationMemoryStream.ToArray();\n            }\n\n            Assert.AreEqual(sourceBytes.Length, destinationBytes.Length, \"Stream lengths do not match.\");\n            Assert.AreEqual(sourceBytes, destinationBytes, \"Stream contents do not match.\");\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2103231256",
    "pr_number": 50222,
    "pr_file": "sdk/communication/Azure.Communication.CallAutomation/tests/CallRecordings/CallRecordingAutomatedLiveTests.cs",
    "created_at": "2025-05-22T19:06:18+00:00",
    "commented_code": "Assert.AreEqual(StatusCodes.Status200OK, startRecordingResponse.GetRawResponse().Status);\n                    Assert.NotNull(startRecordingResponse.Value.RecordingId);\n\n                    // Update the property name from 'PlaySourceId' to 'PlaySourceCacheId' as per the provided type signature.\n                    var playSource = new FileSource(new Uri(TestEnvironment.FileSourceUrl)) { PlaySourceCacheId = \"test-audio\" };\n                    var playResponse = await response.CallConnection.GetCallMedia().PlayToAllAsync(playSource);\n                    Assert.NotNull(playResponse);\n                    Assert.AreEqual(202, playResponse.GetRawResponse().Status);\n\n                    await Task.Delay(TimeSpan.FromSeconds(5)).ConfigureAwait(false);\n\n                    // try stop recording\n                    var stopRecordingResponse = await client.GetCallRecording().StopAsync(startRecordingResponse.Value.RecordingId);\n                    Assert.AreEqual(StatusCodes.Status204NoContent, stopRecordingResponse.Status);\n\n                    await Task.Delay(TimeSpan.FromSeconds(5)).ConfigureAwait(false);",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2103231256",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50222,
        "pr_file": "sdk/communication/Azure.Communication.CallAutomation/tests/CallRecordings/CallRecordingAutomatedLiveTests.cs",
        "discussion_id": "2103231256",
        "commented_code": "@@ -472,10 +472,20 @@ public async Task GetRecordingTest()\n                     Assert.AreEqual(StatusCodes.Status200OK, startRecordingResponse.GetRawResponse().Status);\n                     Assert.NotNull(startRecordingResponse.Value.RecordingId);\n \n+                    // Update the property name from 'PlaySourceId' to 'PlaySourceCacheId' as per the provided type signature.\n+                    var playSource = new FileSource(new Uri(TestEnvironment.FileSourceUrl)) { PlaySourceCacheId = \"test-audio\" };\n+                    var playResponse = await response.CallConnection.GetCallMedia().PlayToAllAsync(playSource);\n+                    Assert.NotNull(playResponse);\n+                    Assert.AreEqual(202, playResponse.GetRawResponse().Status);\n+\n+                    await Task.Delay(TimeSpan.FromSeconds(5)).ConfigureAwait(false);\n+\n                     // try stop recording\n                     var stopRecordingResponse = await client.GetCallRecording().StopAsync(startRecordingResponse.Value.RecordingId);\n                     Assert.AreEqual(StatusCodes.Status204NoContent, stopRecordingResponse.Status);\n \n+                    await Task.Delay(TimeSpan.FromSeconds(5)).ConfigureAwait(false);",
        "comment_created_at": "2025-05-22T19:06:18+00:00",
        "comment_author": "Copilot",
        "comment_body": "Using fixed delays can lead to flaky tests; consider polling the recording status with a timeout or exponential backoff instead of a hardcoded Task.Delay.\n```suggestion\n                    await WaitForConditionAsync(\n                        async () =>\n                        {\n                            var recordingState = await client.GetCallRecording().GetRecordingStateAsync(startRecordingResponse.Value.RecordingId).ConfigureAwait(false);\n                            return recordingState.Value == RecordingState.Active;\n                        },\n                        TimeSpan.FromSeconds(10),\n                        TimeSpan.FromMilliseconds(500)\n                    ).ConfigureAwait(false);\n\n                    // try stop recording\n                    var stopRecordingResponse = await client.GetCallRecording().StopAsync(startRecordingResponse.Value.RecordingId);\n                    Assert.AreEqual(StatusCodes.Status204NoContent, stopRecordingResponse.Status);\n\n                    await WaitForConditionAsync(\n                        async () =>\n                        {\n                            var recordingState = await client.GetCallRecording().GetRecordingStateAsync(startRecordingResponse.Value.RecordingId).ConfigureAwait(false);\n                            return recordingState.Value == RecordingState.Stopped;\n                        },\n                        TimeSpan.FromSeconds(10),\n                        TimeSpan.FromMilliseconds(500)\n                    ).ConfigureAwait(false);\n```",
        "pr_file_module": null
      }
    ]
  }
]
