---
title: Validate quantization parameters carefully
description: 'When implementing quantized operations in ML models, thoroughly validate
  quantization parameters to ensure correctness and prevent subtle numerical errors.
  Key validation points:'
repository: tensorflow/tensorflow
label: AI
language: Other
comments_count: 5
repository_stars: 190625
---

When implementing quantized operations in ML models, thoroughly validate quantization parameters to ensure correctness and prevent subtle numerical errors. Key validation points:

1. For int16 quantized operators, verify zero points are exactly 0
2. For quantized tensor operations, ensure consistent scale factors between input and output
3. When one tensor is quantized, verify all related tensors use compatible quantization schemes

Example:
```cpp
// Good: Proper quantization parameter validation
if (input->type == kTfLiteInt16) {
  TF_LITE_ENSURE_EQ(context, input->params.zero_point, 0);
  TF_LITE_ENSURE_EQ(context, output->params.zero_point, 0);
}

// For quantized operations, validate scale consistency
if (input->type == kTfLiteInt8 || input->type == kTfLiteInt16) {
  TF_LITE_ENSURE_EQ(context, input->params.scale, output->params.scale);
}

// Ensure quantization scheme compatibility
if (lhs.IsQuantized()) {
  if (!rhs.IsQuantized() || !output.IsQuantized()) {
    return absl::FailedPreconditionError(
        "If one tensor is quantized, all must be quantized");
  }
}
```