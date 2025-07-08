---
title: Specify configuration behaviors
description: When implementing configuration features (variables, flags, resources),
  thoroughly document their behavior in all scenarios, especially edge cases and interactions
  with dependencies. Configuration options should have well-defined and tested behaviors
  across all contexts where they might be used.
repository: opentofu/opentofu
label: Configurations
language: Markdown
comments_count: 7
repository_stars: 25901
---

When implementing configuration features (variables, flags, resources), thoroughly document their behavior in all scenarios, especially edge cases and interactions with dependencies. Configuration options should have well-defined and tested behaviors across all contexts where they might be used.

For features like ephemeral resources, variable marks, or command flags like `-exclude`, ensure you clearly specify:

- How marks propagate and interact with other systems
  ```hcl
  # When using ephemeral variables, document if and how the mark propagates
  variable "secret" {
    type = string
    ephemeral = true
  }
  
  locals {
    # Does this local automatically become ephemeral too?
    config = "${var.secret}_suffix"
  }
  ```

- Dependencies and cascading effects
  ```hcl
  # When implementing features like -exclude, document how dependencies are handled
  # For example, when excluding resource A that resource B depends on:
  resource "null_resource" "a" {}
  
  resource "null_resource" "b" {
    triggers = {
      a_id = null_resource.a.id
    }
  }
  # Document: Will `tofu plan -exclude=null_resource.a` also exclude resource B?
  ```

- Behavior during different execution phases (plan vs apply)
- Edge cases like non-existent resources, empty collections, or conflicting settings

When introducing new marks or configuration attributes, thoroughly test their interactions with existing marks to prevent subtle bugs. For example, ensure `sensitive()` doesn't accidentally strip ephemeral marks, and that marked values maintain their properties when transformed or combined.