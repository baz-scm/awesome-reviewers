---
title: Explicit protocol interfaces
description: Design protocol interfaces with explicit behavior definitions rather
  than relying on implicit conventions. Clearly specify the purpose and expected handling
  of each field, especially when adding new parameters or response structures.
repository: hashicorp/terraform
label: API
language: Other
comments_count: 4
repository_stars: 45532
---

Design protocol interfaces with explicit behavior definitions rather than relying on implicit conventions. Clearly specify the purpose and expected handling of each field, especially when adding new parameters or response structures.

When adding fields to protocols:
1. Document whether fields are advisory or required
2. Specify if consumers or providers are responsible for enforcing constraints
3. Use explicit fields rather than inferred behavior from configuration
4. Structure messages for future extensibility

For example, when adding a request parameter like `include_resource_object`, make its purpose and handling explicit in the protocol:

```protobuf
message ListResource {
  message Request {
    // When include_resource_object is set to true, the provider should
    // include the full resource object for each result
    bool include_resource_object = 3;
  }
}
```

Similarly, consider forward compatibility when designing response structures. Avoid constructs like `oneof` when they might restrict valid combinations:

```protobuf
// Avoid this pattern if both fields might be needed simultaneously
message Event {
  oneof response {
    Result result = 1;
    Diagnostic diagnostic = 2;  // Cannot return diagnostics with results
  }
}

// Better approach allowing both fields together
message Event {
  Result result = 1;
  repeated Diagnostic diagnostics = 2;
}
```

For future extensibility, nest related fields in sub-messages that can evolve independently:

```protobuf
message Request {
  message Mapping {
    map<string, string> resource_address_map = 1;
    map<string, string> module_address_map = 2;
  }
  
  // Can later extend with additional mapping types
  oneof mapping {
    Mapping simple = 1;
  }
}
```

Explicit interfaces lead to more robust integrations, fewer bugs from misunderstood expectations, and easier evolution of your API over time.