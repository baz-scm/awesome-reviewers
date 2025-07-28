---
title: Maintain inline documentation
description: Ensure inline code comments are accurate, current, and provide meaningful
  explanations for complex or unclear code sections. Comments should be updated whenever
  the associated code changes to prevent misleading documentation.
repository: home-assistant/core
label: Documentation
language: Python
comments_count: 2
repository_stars: 80450
---

Ensure inline code comments are accurate, current, and provide meaningful explanations for complex or unclear code sections. Comments should be updated whenever the associated code changes to prevent misleading documentation.

Add explanatory comments for:
- Unclear device categories, constants, or identifiers
- Complex logic or business rules
- Non-obvious code sections that future developers might struggle to understand

Update existing comments when:
- Code behavior changes
- Function signatures are modified
- Logic flow is altered

Example of adding missing explanatory comment:
```python
# Micro Storage Inverter
# Energy storage and solar PV inverter system with monitoring capabilities
"xnyjcn": (
    # device configuration...
)
```

Example of updating stale comment:
```python
# The light supports both white (with or without adjustable color temperature)
# and HS, determine which mode the light is in. We consider it to be in HS color
# mode, when work mode is anything else than "white".
if (
    self.device.status.get(self._color_mode_dpcode) != WorkMode.WHITE
):
    return ColorMode.HS
return (
    self._white_color_mode if self._white_color_mode else ColorMode.COLOR_TEMP
)
```

Well-maintained inline documentation reduces cognitive load for code reviewers and future maintainers, making the codebase more accessible and reducing the likelihood of bugs introduced by misunderstanding existing code.