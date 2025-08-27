---
title: Comprehensive test structure
description: Tests should focus on comprehensive coverage of main logic flows rather
  than trivial functions, use established testing patterns like TestCommonStruct for
  end-to-end validation, and maintain proper table-driven test formatting for readability
  and maintainability.
repository: volcano-sh/volcano
label: Testing
language: Go
comments_count: 4
repository_stars: 4899
---

Tests should focus on comprehensive coverage of main logic flows rather than trivial functions, use established testing patterns like TestCommonStruct for end-to-end validation, and maintain proper table-driven test formatting for readability and maintainability.

Key principles:
1. **Focus on main logic**: Test the core scheduling processes and business logic rather than simple getter/setter functions
2. **Use established patterns**: Leverage existing test utilities like TestCommonStruct to verify complete workflows
3. **Proper table formatting**: Structure test tables with clear field alignment and consistent formatting

Example of well-structured test:
```go
tests := []struct {
    name string
    args args
    want ResourceStrategyFit
}{
    {
        name: "test with cpu and memory resources",
        args: args{framework.Arguments{
            "ResourceStrategyFitPlusWeight": 10,
            "resources": map[string]interface{}{
                "cpu": map[string]interface{}{
                    "type":   "MostAllocated",
                    "weight": 1,
                },
                "memory": map[string]interface{}{
                    "type":   "LeastAllocated", 
                    "weight": 2,
                },
            },
        }},
        want: ResourceStrategyFit{
            ResourceStrategyFitWeight: 10,
            Resources: map[v1.ResourceName]ResourcesType{
                "cpu": {
                    Type:   config.MostAllocated,
                    Weight: 1,
                },
                "memory": {
                    Type:   config.LeastAllocated,
                    Weight: 2,
                },
            },
        },
    },
}
```

For integration tests, use the TestCommonStruct pattern to validate complete scheduling workflows rather than isolated unit tests.