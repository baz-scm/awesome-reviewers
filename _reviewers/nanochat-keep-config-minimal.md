---
title: Keep config minimal
description: Avoid “config monsters” by limiting new runtime knobs and centralizing
  stable defaults. Only add CLI/config parameters when they materially change behavior
  across experiments; otherwise, bake them into the existing config (or the run script)
  and reuse current config locations rather than introducing new config modules for
  a few constants. For...
repository: karpathy/nanochat
label: Configurations
language: Python
comments_count: 4
repository_stars: 53189
---

Avoid “config monsters” by limiting new runtime knobs and centralizing stable defaults. Only add CLI/config parameters when they materially change behavior across experiments; otherwise, bake them into the existing config (or the run script) and reuse current config locations rather than introducing new config modules for a few constants. For evaluation-critical settings, explicitly pin values and avoid hidden coupling between constants.

Apply:
- Don’t add dozens of flags for one model variant—prefer a single enabling flag (or none) with fixed defaults baked into config.
- Reuse existing config files/modules; if you need only a few constants, place them alongside the code that consumes them instead of adding a new Python module.
- Pin eval constants explicitly (e.g., `VAL_SHARD_INDEX = 1822`) rather than tying them indirectly to other values that might change.
- At configuration boundaries (CLI), constrain allowed values (e.g., `choices`) so invalid settings fail fast.

Example (CLI boundary + baked/stable defaults):
```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--device', type=str, default='cuda', choices=['mps','cuda'])

# Keep eval config explicit and stable
VAL_SHARD_INDEX = 1822
```
