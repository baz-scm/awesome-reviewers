---
title: Prefer explicit readable code
description: 'Write code that prioritizes readability and explicitness over cleverness
  or brevity. This includes several key practices:


  **Import Organization**: Follow standard import ordering - stdlib and third-party
  imports first, then openpilot imports after a blank line:'
repository: commaai/openpilot
label: Code Style
language: Python
comments_count: 9
repository_stars: 58214
---

Write code that prioritizes readability and explicitness over cleverness or brevity. This includes several key practices:

**Import Organization**: Follow standard import ordering - stdlib and third-party imports first, then openpilot imports after a blank line:
```python
import os
import threading
import numpy as np

from openpilot.common.params import Params
from openpilot.selfdrive.ui.ui_state import ui_state
```

**Explicit Conditionals**: Use clear if-elif chains instead of complex conditional expressions:
```python
# Prefer this:
if self.CP.carFingerprint in FCEV_CAR:
    ret.gas = cp.vl["ACCELERATOR"]["ACCELERATOR_PEDAL"] / 254.
elif self.CP.carFingerprint in HYBRID_CAR:
    ret.gas = cp.vl["E_EMS11"]["CR_Vcu_AccPedDep_Pos"] / 254.
else:
    ret.gas = cp.vl["E_EMS11"]["Accel_Pedal_Pos"] / 254.

# Over this:
gas_sig = "Accel_Pedal_Pos" if self.CP.carFingerprint in EV_CAR else \
          "ACCELERATOR_PEDAL" if self.CP.carFingerprint in FCEV_CAR else \
          "CR_Vcu_AccPedDep_Pos"
```

**Simple Variable Assignment**: Avoid walrus operators and complex expressions when simple two-line assignments are clearer:
```python
# Prefer this:
events_changed = self.events.names != self.events_prev
if events_changed:

# Over this:
if events_changed := (self.events.names != self.events_prev):
```

**Meaningful Variable Names**: Use descriptive variables instead of magic numbers or complex expressions:
```python
# Prefer this:
counter = int(CS.sccm_right_stalk["SCCM_rightStalkCounter"])
can_sends.append(self.tesla_can.right_stalk_press(counter + 1, 1))
can_sends.append(self.tesla_can.right_stalk_press(counter + 2, 0))

# Over this:
counter = int(CS.sccm_right_stalk["SCCM_rightStalkCounter"] + 1) % 16
can_sends.append(self.tesla_can.right_stalk_press(counter, 1))
can_sends.append(self.tesla_can.right_stalk_press((counter + 1) % 16, 0))
```

The goal is to write code that other developers can quickly understand without having to decode complex expressions or trace through clever logic.