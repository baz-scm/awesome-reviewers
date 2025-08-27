---
title: Standardize configuration formats
description: Ensure all plugin configurations follow a consistent, structured format
  across the codebase to improve maintainability and user experience. Different plugins
  and features should not use ad-hoc configuration styles that make the system fragmented
  and difficult to understand.
repository: volcano-sh/volcano
label: Configurations
language: Markdown
comments_count: 3
repository_stars: 4899
---

Ensure all plugin configurations follow a consistent, structured format across the codebase to improve maintainability and user experience. Different plugins and features should not use ad-hoc configuration styles that make the system fragmented and difficult to understand.

**Key principles:**
1. **Consistent parameter structure**: Use structured YAML/JSON objects instead of string-based or mixed formats
2. **Unified configuration style**: Follow established patterns from existing plugins like `binpack`
3. **Formal API definitions**: Define configuration parameters as proper API structures rather than informal argument lists

**Example of good practice:**
```yaml
# Structured configuration approach
- name: resource-strategy-fit
  arguments:
    resourceStrategyFitWeight: 10
    resources:
      nvidia.com/gpu:
        type: MostAllocated
        weight: 2
      cpu:
        type: LeastAllocated
        weight: 1
```

**Example of what to avoid:**
```yaml
# Ad-hoc string-based configuration
arguments:
  reserve.nodeLabel: label1,label2
  reserve.define.label1: {"business_type": "ebook"}
```

**Better alternative:**
```yaml
# Structured alternative
arguments:
  reserveLabels:
  - nodeSelector:
      business_type: ebook
    startHour: 3
    endHour: 4
    resources:
      cpu: 32
      memory: 64
```

This standardization reduces cognitive load for users, simplifies validation, and makes the configuration system more maintainable as new features are added.