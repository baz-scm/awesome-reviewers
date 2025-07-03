---
title: Follow API conventions
description: When designing APIs, adhere to established API conventions, particularly
  Kubernetes API conventions when working within the Kubernetes ecosystem. This improves
  API clarity, maintainability, and future compatibility.
repository: kubeflow/kubeflow
label: API
language: Go
comments_count: 4
repository_stars: 15064
---

When designing APIs, adhere to established API conventions, particularly Kubernetes API conventions when working within the Kubernetes ecosystem. This improves API clarity, maintainability, and future compatibility.

Key practices:
1. **Use standard data formats** instead of custom parsing methods
   ```go
   // Instead of custom string parsing:
   requestHeaders := strings.Split(annotations["notebooks.kubeflow.org/http-headers-request-set"], "\n")
   
   // Prefer using standard JSON:
   var requestHeaders map[string]string
   if err := json.Unmarshal([]byte(annotations["notebooks.kubeflow.org/http-headers-request-set"]), &requestHeaders); err != nil {
       // Handle error
   }
   ```

2. **Use explicit field definitions** rather than embedding complex objects
   ```go
   // Instead of embedding the entire ObjectMeta:
   type PodDefaultSpec struct {
       // ObjectMeta defines the metadata to inject into the pod
       metav1.ObjectMeta `json:"metadata,omitempty"`
   }
   
   // Be specific about which fields you need:
   type PodDefaultSpec struct {
       // Labels to inject into pod metadata
       Labels map[string]string `json:"labels,omitempty"`
       // Annotations to inject into pod metadata
       Annotations map[string]string `json:"annotations,omitempty"`
   }
   ```

3. **Use conditions instead of enums** for representing status
   ```go
   // Instead of enum-style status:
   type ProfileState string
   
   // Use standard Kubernetes condition pattern:
   type ProfileCondition struct {
       Type    string `json:"type"`
       Status  v1.ConditionStatus `json:"status"`
       LastUpdateTime metav1.Time `json:"lastUpdateTime,omitempty"`
       LastTransitionTime metav1.Time `json:"lastTransitionTime,omitempty"`
       Reason string `json:"reason,omitempty"`
       Message string `json:"message,omitempty"`
   }
   ```

Following these conventions enhances API clarity, avoids reinventing the wheel, and ensures your APIs evolve gracefully as requirements change.
