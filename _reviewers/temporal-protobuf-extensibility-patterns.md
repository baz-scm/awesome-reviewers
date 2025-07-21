---
title: Protobuf extensibility patterns
description: When designing Protocol Buffer APIs, use `oneof` fields to create extensible
  message structures that maintain compatibility while providing type safety. This
  pattern allows APIs to evolve over time by adding new message variants without breaking
  existing clients.
repository: temporalio/temporal
label: API
language: Other
comments_count: 2
repository_stars: 14953
---

When designing Protocol Buffer APIs, use `oneof` fields to create extensible message structures that maintain compatibility while providing type safety. This pattern allows APIs to evolve over time by adding new message variants without breaking existing clients.

Instead of creating separate message types that require type checking during deserialization:

```protobuf
// Avoid this pattern
message ChasmTransferTaskInfo {
  // fields...
}

// And then manually figuring out which message to deserialize into
```

Use the `oneof` pattern to create a clear type hierarchy within a single message:

```protobuf
message OutboundTaskInfo {
  // Common fields...
  string destination = 7;
  
  oneof task_details {
    // Task-specific details
    StateMachineTaskInfo state_machine_info = 8;
    ChasmTaskInfo chasm_info = 9;
    // Future task types can be added here
  }
}
```

This approach offers several benefits:
- Maintains binary compatibility as noted in the protobuf documentation
- Provides clear type discrimination during deserialization
- Centralizes related message variants in a logical structure
- Allows for future extension without modifying existing code paths

Remember that while this is binary compatible at the protocol level, generated code in some languages (like Go) might have API-breaking changes, so coordinate with client teams when making these changes.