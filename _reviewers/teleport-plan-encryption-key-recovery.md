---
title: Plan encryption key recovery
description: Always implement recovery mechanisms and plan for key rotation when designing
  encryption systems. Encryption key failures, compromises, or rotation issues can
  lead to permanent data loss or service disruption.
repository: gravitational/teleport
label: Security
language: Other
comments_count: 3
repository_stars: 19109
---

Always implement recovery mechanisms and plan for key rotation when designing encryption systems. Encryption key failures, compromises, or rotation issues can lead to permanent data loss or service disruption.

Key recovery strategies include:
- **Recovery keys**: Implement backup keys (HSM or software-based) that can decrypt data if primary keys are lost or destroyed
- **Multiple encryption layers**: Generate per-session software keys, encrypt data with them, then encrypt the software keys with HSM keys - this allows selective key revocation without re-encrypting all data
- **Consistent key access**: Ensure all service replicas access the same encryption keys to prevent inconsistent encryption/decryption capabilities
- **Rotation planning**: Avoid static key configurations that appear to work initially but break during automatic key rotation cycles

Example configuration showing recovery key setup:
```yaml
auth_service:
  session_recording_config:
    encryption:
      enabled: yes
      recovery_key: "backup-hsm-key"
      key_rotation_policy: "automatic"
```

Without proper key recovery planning, a single HSM failure or incorrect key deletion can make all encrypted session recordings permanently inaccessible, creating both security and compliance risks.