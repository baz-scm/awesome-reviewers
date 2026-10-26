---
title: Security Field Validation
description: 'When adding or modifying security-sensitive API fields (including fields
  written by schedulers/kubelets or reflected in Pod/Container security context),
  enforce the full security invariant end-to-end:'
repository: kUbernetes/kUbernetes
label: Security
language: Go
comments_count: 5
repository_stars: 128688
---

When adding or modifying security-sensitive API fields (including fields written by schedulers/kubelets or reflected in Pod/Container security context), enforce the full security invariant end-to-end:

1) Don’t trust status/snapshots from external writers
- Add apiserver-side validation for any scheduler/client-written “snapshot” fields, including explicit size/limits (documented and enforced via constants) and structural constraints.
- Treat status writes as untrusted input: validate both shape and bounds.

2) Validate transitions, not just the new object
- For security-relevant Pod status fields, validation must consider the oldPod and restrict what may change after binding/running (e.g., only allow changes while nodeName is empty; otherwise require cover/coverage checks to be re-run and reject increasing changes).

3) Preserve security intent during merges
- Ensure kubelet/effective-security-context logic does not drop per-container security settings when pod-level securityContext is present (copy/merge container-level fields into the effective result).

4) Align admission/policy with runtime behavior and be version-safe
- Add/extend Pod Security admission checks for new security fields so Restricted (and other profiles) explicitly forbids invalid values from the earliest safe policy version; avoid accidentally permitting the field in older policy versions.
- Document allowed enum values and ensure unknown values are rejected.

Example pattern (transition validation sketch):
```go
func ValidateXUpdate(newPod, oldPod *core.Pod, opts PodValidationOptions) field.ErrorList {
    // Block or constrain security-relevant status changes after bind
    if oldPod.Spec.NodeName != "" && newPod.Spec.NodeName != "" {
        // Re-run coverage/limit checks or require the change to be non-increasing
        // else return an error
    }

    // Validate bounds/shape of any status snapshots here
    // (including explicit max sizes via a Go constant)
    return nil
}
```

Apply this standard to any change involving security-context fields (e.g., cgroup options) or security-affecting status data used by scheduler/quota/kubelet calculations.