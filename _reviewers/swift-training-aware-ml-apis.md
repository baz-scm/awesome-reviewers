---
title: Training-aware ML APIs
description: Design machine learning APIs with explicit parameters for distinguishing
  between training and inference phases rather than relying on global state or implicit
  context. This pattern enables concurrent training and testing, improves model reusability,
  and prevents subtle bugs in distributed training scenarios.
repository: tensorflow/swift
label: AI
language: Markdown
comments_count: 3
repository_stars: 6136
---

Design machine learning APIs with explicit parameters for distinguishing between training and inference phases rather than relying on global state or implicit context. This pattern enables concurrent training and testing, improves model reusability, and prevents subtle bugs in distributed training scenarios.

```swift
// Instead of using global context:
protocol Layer {
    func call(_ input: Input) -> Output  // Implicit context is problematic
}

// Use explicit training parameters:
protocol Layer {
    associatedtype Input: Differentiable
    associatedtype Output: Differentiable
    
    @differentiable(wrt: (self, input))
    func call(_ input: Input, training: Bool) -> Output
}

// Implementation example:
struct BatchNorm: Layer {
    var scale: Tensor<Float>
    var offset: Tensor<Float>
    @noDerivative var runningMean: Tensor<Float>
    @noDerivative var runningVariance: Tensor<Float>
    
    @differentiable(wrt: (self, input))
    func call(_ input: Tensor<Float>, training: Bool) -> Tensor<Float> {
        if training {
            // Use batch statistics, update running statistics
            let batchStatistics = calculateBatchStatistics(input)
            updateRunningStatistics(batchStatistics)
            return normalize(input, using: batchStatistics)
        } else {
            // Use running statistics
            return normalize(input, using: (runningMean, runningVariance))
        }
    }
}
```
