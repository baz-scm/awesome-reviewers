---
title: thoughtful configuration design
description: When designing configuration schemas and fields, carefully consider their
  placement, validation, and long-term implications to prevent conflicts, maintain
  compatibility, and ensure good user experience.
repository: gravitational/teleport
label: Configurations
language: Markdown
comments_count: 9
repository_stars: 19109
---

When designing configuration schemas and fields, carefully consider their placement, validation, and long-term implications to prevent conflicts, maintain compatibility, and ensure good user experience.

Key principles to follow:

**Field Placement**: Avoid adding new fields to shared types like metadata that could cause unintended side effects across multiple resource types. Place configuration fields at appropriate levels where they can be validated independently.

**Conflict Prevention**: Design configuration to avoid ambiguous states where resources could match multiple conflicting criteria. Use explicit validation to catch potential conflicts early rather than relying on implicit resolution.

**Backwards Compatibility**: Consider how configuration changes affect existing tooling like Terraform providers that check for drift. Provide sensible defaults and migration paths for new fields.

**Size and Constraint Management**: Implement appropriate limits for configuration size and complexity. For example, limit configuration payloads to stay within backend storage constraints (e.g., 320KB for DynamoDB).

**Graceful Validation**: Handle invalid or unrecognized configuration gracefully by providing clear error messages and, where appropriate, warnings about ignored fields rather than silent failures.

**Complexity Reduction**: Simplify configuration schemas to reduce the likelihood of user misconfigurations. Provide sensible defaults and clear documentation about field interactions.

Example of thoughtful field placement:
```yaml
# Good: Top-level field with clear scope
kind: example_resource
metadata:
  name: example
scope: /staging/west  # Clear, independent field

# Avoid: Adding to shared metadata type
metadata:
  name: example
  scope: /staging/west  # Could affect all resource types
```

This approach prevents configuration-related issues that can lead to security vulnerabilities, operational problems, and poor user experience.