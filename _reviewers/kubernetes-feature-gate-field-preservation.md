---
title: Feature gate field preservation
description: When implementing feature-gated fields, always preserve existing field
  values when the feature gate is disabled, but drop new field values that depend
  on disabled features. This prevents breaking existing functionality during feature
  gate transitions or version skew scenarios.
repository: kubernetes/kubernetes
label: Configurations
language: Go
comments_count: 11
repository_stars: 116489
---

When implementing feature-gated fields, always preserve existing field values when the feature gate is disabled, but drop new field values that depend on disabled features. This prevents breaking existing functionality during feature gate transitions or version skew scenarios.

**Key principles:**
1. **Preserve existing usage**: If a field was already set in the old object, keep it even when the feature gate is disabled
2. **Drop new dependencies**: Only drop fields when they're newly introduced and the feature gate is off
3. **Isolate feature checks**: Create separate validation blocks for new features rather than modifying existing logic
4. **Cache feature state**: Use struct fields to store feature gate state instead of repeated `DefaultFeatureGate.Enabled()` calls

**Example implementation:**
```go
func dropDisabledDRAFields(newSlice, oldSlice *resource.ResourceSlice) {
    // Check if feature is enabled OR was already in use
    if utilfeature.DefaultFeatureGate.Enabled(features.DRANewFeature) ||
        draNewFeatureInUse(oldSlice) {
        return
    }
    
    // Only drop fields if not previously used
    for i := range newSlice.Spec.Devices {
        newSlice.Spec.Devices[i].NewFeatureField = nil
    }
}

// Separate validation for new features
if !utilfeature.DefaultFeatureGate.Enabled(features.DRANewFeature) && 
   !newFeatureInUse(oldPodSpec, oldPodStatus) {
    // Drop new feature fields
    dropNewFeatureFields(podSpec)
}
```

This approach ensures backward compatibility, prevents data loss during upgrades/downgrades, and maintains clean separation between feature-gated and stable functionality.