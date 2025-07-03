---
title: Code for readability
description: Prioritize human readability when writing code. Split complex expressions
  into steps with meaningful variable names. Extract repeated logic into well-named
  functions. Avoid magic numbers - derive values from existing structures or use named
  constants. Simplify control flow by reducing nesting levels and using early returns.
repository: opencv/opencv
label: Code Style
language: C++
comments_count: 13
repository_stars: 82865
---

Prioritize human readability when writing code. Split complex expressions into steps with meaningful variable names. Extract repeated logic into well-named functions. Avoid magic numbers - derive values from existing structures or use named constants. Simplify control flow by reducing nesting levels and using early returns.

```cpp
// Instead of:
if (VP8_STATUS_OK == WebPGetFeatures(header, sizeof(header), &features)) {
    // Many lines of nested code
}

// Prefer:
if (VP8_STATUS_OK < WebPGetFeatures(header, sizeof(header), &features))
    return false;

// For complex conditions, split into steps:
// Instead of:
if(cv::gapi::getCompileArg<std::reference_wrapper<cv::gapi::wip::ov::workload_type>>(compileArgs).has_value()) {
    // ...

// Prefer:
auto workload = cv::gapi::getCompileArg<std::reference_wrapper<cv::gapi::wip::ov::workload_type>>(compileArgs);
if(workload.has_value()) {
    // ...

// Instead of magic numbers:
const Mat points_mat = Mat(Size(6, 24), CV_32F, &points_data);

// Prefer:
const size_t channels = 6;  // 3 coordinates + 3 color values
const size_t pointCount = sizeof(points_data)/(channels*sizeof(float));
const Mat points_mat = Mat(Size(channels, pointCount), CV_32F, &points_data);
```
