---
title: Unit tests for cmdlet paths
description: 'Add isolated unit tests for cmdlet production paths using mocked client
  operations. Tests must validate more than a “happy path” scenario run:


  - Verify exact client call arguments (including resource identifiers and IDs).'
repository: Azure/azure-powershell
label: Testing
language: C#
comments_count: 2
repository_stars: 4762
---

Add isolated unit tests for cmdlet production paths using mocked client operations. Tests must validate more than a “happy path” scenario run:

- Verify exact client call arguments (including resource identifiers and IDs).
- When input is list/batch, test multi-item inputs and assert the exact ordered collection sent to the batch API.
- Verify output mapping (e.g., successful service response maps into the expected PowerShell response type).
- Verify ShouldProcess=false: the client method must not be called.
- Verify exception behavior: client exceptions propagate (or are handled as specified).
- Cover boundaries for batch APIs: empty/null behavior and per-item error handling.
- Do not rely on recorded/integration scenarios to substitute for unit coverage of these branches.

Example (pattern):
```csharp
// Arrange
var ops = new Mock<IScheduledEventsOperations>(MockBehavior.Strict);
var sut = new SetAzureRmScheduledEvents(/* inject ops via ctor/prop */);

sut.ShouldProcessDelegate = _ => false; // or set up ShouldProcess to return false

// Act
sut.ExecuteCmdlet();

// Assert
ops.VerifyNoOtherCalls();

// Another test: batch semantics + ordered IDs
var expectedIds = new[] { "id1", "id2" };
ops.Setup(x => x.AcknowledgeList(
        "rg", "type", "name",
        expectedIds
    ))
  .Returns(new ScheduledEventsApproveResponse { /* ... */ });

sut.ShouldProcessDelegate = _ => true;
sut.ScheduledEventsIds = expectedIds;

sut.ExecuteCmdlet();

// Assert: mapping to PSScheduledEventsApproveResponse and exact ordered payload already verified by mock.
```
Apply this standard to any cmdlet logic that orchestrates client calls, especially those behind ShouldProcess and those that build request payloads for list/batch APIs.