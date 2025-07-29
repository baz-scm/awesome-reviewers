---
title: Configuration validation consistency
description: Ensure configuration fields use consistent validation patterns, appropriate
  data types, and proper bounds checking. This includes using correct regex patterns
  for duration fields, consistent type usage across similar fields, and implementing
  cross-field validation where relationships exist.
repository: traefik/traefik
label: Configurations
language: Go
comments_count: 12
repository_stars: 55772
---

Ensure configuration fields use consistent validation patterns, appropriate data types, and proper bounds checking. This includes using correct regex patterns for duration fields, consistent type usage across similar fields, and implementing cross-field validation where relationships exist.

Key practices:
1. **Duration validation patterns**: Use the simplified regex pattern `^[0-9]+(\\.[0-9]+)?(ns|us|µs|ms|s|m|h)?$` instead of the complex `^([0-9]+(\\.[0-9]+)?(ns|us|µs|ms|s|m|h))+$` for duration fields
2. **Type consistency**: Use `ptypes.Duration` consistently for timeout/duration configurations rather than mixing with `time.Duration`
3. **Validation bounds**: Add appropriate kubebuilder validation constraints like `+kubebuilder:validation:Minimum=0` and maximum bounds where applicable
4. **Cross-field validation**: Implement validation checks for related fields (e.g., ensuring ResponseHeaderTimeout ≤ Timeout) in the Init() method

Example of proper duration field validation:
```go
// DialTimeout is the amount of time to wait until a connection can be established.
// +kubebuilder:validation:Pattern="^[0-9]+(\\.[0-9]+)?(ns|us|µs|ms|s|m|h)?$"
// +kubebuilder:validation:XIntOrString
DialTimeout *intstr.IntOrString `json:"dialTimeout,omitempty"`
```

This ensures configuration fields are validated consistently, preventing runtime errors and improving user experience with clear validation messages.