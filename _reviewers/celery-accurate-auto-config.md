---
title: Accurate, Auto Config
description: 'User-facing configuration should be correct, self-contained, and hard
  to misuse.


  Apply these rules:

  1) **Document the exact scope of each setting/env var**: the description must match
  the code paths that actually enforce the behavior (what calls it affects, and what
  it does *not* affect).'
repository: celery/celery
label: Configurations
language: Other
comments_count: 4
repository_stars: 28464
---

User-facing configuration should be correct, self-contained, and hard to misuse.

Apply these rules:
1) **Document the exact scope of each setting/env var**: the description must match the code paths that actually enforce the behavior (what calls it affects, and what it does *not* affect).
2) **Ensure documented config keys are exact**: env var/setting names in docs must match the implementation; don’t introduce near-miss names.
3) **Avoid “extra required flags” for core behavior**: if the system can reliably detect a condition (e.g., quorum queues in use), make the dependent feature enable itself automatically. Treat user warnings as a last resort, not as the primary mechanism.
4) **Keep configuration/distribution declarations consistent**: if you maintain a canonical requirements list, ensure packaging (e.g., RPM) doesn’t diverge into duplicated or platform-specific dependency sets.

Example (automatic dependent configuration with quorum queues):
```python
from kombu import Queue

task_queues = [Queue('my-queue', queue_arguments={'x-queue-type': 'quorum'})]

# Configure only the primary queue behavior; the dependent feature
# (e.g., native delayed delivery for ETA/Countdown) should enable automatically
# when quorum queues are detected.
broker_transport_options = {"confirm_publish": True}
```

Checklist when updating configuration/docs:
- Do the docs say “which APIs/call paths” the setting actually changes?
- Are setting/env var names copy-pasted from the real keys?
- If a dependent behavior exists, can you auto-enable it via detection rather than requiring another flag?
- Do packaging requirements stay consistent with the canonical requirements file (no drift between targets)?