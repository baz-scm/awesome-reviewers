---
title: Configuration mutual exclusivity validation
description: Ensure configuration options that are mutually exclusive are properly
  validated with clear, actionable error messages. When introducing configuration
  fields that cannot be used together, implement validation logic that checks for
  conflicts and provides specific guidance to users.
repository: prometheus/prometheus
label: Configurations
language: Go
comments_count: 8
repository_stars: 59616
---

Ensure configuration options that are mutually exclusive are properly validated with clear, actionable error messages. When introducing configuration fields that cannot be used together, implement validation logic that checks for conflicts and provides specific guidance to users.

Key practices:
1. **Validate mutual exclusivity**: Check for conflicting configuration combinations during unmarshaling or validation
2. **Provide clear error messages**: Include the specific field names and explain why they cannot be used together
3. **Handle inheritance properly**: Reset default values when inheritance is needed to distinguish between explicit and default settings
4. **Validate early**: Perform configuration validation at startup to catch issues before runtime

Example implementation:
```go
func (c *OTLPConfig) UnmarshalYAML(unmarshal func(interface{}) error) error {
    // ... unmarshaling logic ...
    
    if c.PromoteAllResourceAttributes {
        if len(c.PromoteResourceAttributes) > 0 {
            return errors.New("'promote_all_resource_attributes' and 'promote_resource_attributes' cannot be configured simultaneously")
        }
        if err := validateAttributes(c.IgnoreResourceAttributes); err != nil {
            return fmt.Errorf("invalid 'ignore_resource_attributes': %w", err)
        }
    } else {
        if len(c.IgnoreResourceAttributes) > 0 {
            return errors.New("'ignore_resource_attributes' cannot be configured unless 'promote_all_resource_attributes' is true")
        }
    }
    return nil
}
```

This approach prevents configuration errors from causing runtime failures and helps users understand the correct configuration patterns.