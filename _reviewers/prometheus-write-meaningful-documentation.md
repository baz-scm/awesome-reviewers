---
title: Write meaningful documentation
description: Documentation comments should be accurate, concise, and add genuine value
  rather than restating obvious code behavior. Focus on explaining "what" the code
  does and "why" it exists, not "how" it works step-by-step.
repository: prometheus/prometheus
label: Documentation
language: Go
comments_count: 8
repository_stars: 59616
---

Documentation comments should be accurate, concise, and add genuine value rather than restating obvious code behavior. Focus on explaining "what" the code does and "why" it exists, not "how" it works step-by-step.

Key principles:
- All exported functions, types, and API changes must have clear documentation comments
- Comments should accurately reflect actual code behavior, not conditional or hypothetical scenarios
- Avoid verbose explanations that simply translate Go code into English
- Keep command-line help text compact and professional
- Remove comments that merely restate what the code obviously does

Example of good documentation:
```go
// addTypeAndUnitLabels appends type and unit labels to the given labels slice.
func addTypeAndUnitLabels(labels []prompb.Label, metricType, unit string) []prompb.Label {
    // implementation
}
```

Example of poor documentation:
```go
// addTypeAndUnitLabels appends type and unit labels to the given labels slice if the setting is enabled.
// This function iterates through the labels and adds new ones based on the parameters provided.
func addTypeAndUnitLabels(labels []prompb.Label, metricType, unit string) []prompb.Label {
    // implementation that doesn't actually check any setting
}
```

Assume readers are proficient in Go and focus documentation on the purpose and behavior rather than implementation details.