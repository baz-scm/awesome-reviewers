---
title: Maintain configuration compatibility
description: When modifying configuration systems, prioritize backward compatibility
  unless there's an explicit breaking change planned. If a breaking change is necessary,
  implement compatibility handlers for older configurations and clearly communicate
  the transition plan.
repository: dotnet/runtime
label: Configurations
language: Txt
comments_count: 2
repository_stars: 16578
---

When modifying configuration systems, prioritize backward compatibility unless there's an explicit breaking change planned. If a breaking change is necessary, implement compatibility handlers for older configurations and clearly communicate the transition plan.

For example, when modifying configuration enums or data structures:

```csharp
// When adding new configuration values, append them rather than reordering
// to maintain compatibility with serialized configurations
enum ConfigValues 
{
    // Existing values - don't change these ids
    Value1 = 1,
    Value2 = 2,
    
    // New values - add at the end
    NewValue = 3
}

// For major changes, implement version detection and compatibility handling
public ProcessConfig(ConfigData data) 
{
    if (data.Version < CurrentVersion) {
        // Handle older format compatibility
        return ProcessLegacyConfig(data);
    }
    
    // Process current format
}
```

This approach ensures tools and systems can continue to process configurations from previous versions, maintaining reliability across version updates. As seen in the discussions, breaking configuration compatibility (like removing enum definitions) can break tools that need to process older versions, requiring changes to be reverted or additional compatibility code to be written.
