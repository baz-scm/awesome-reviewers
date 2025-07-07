---
title: Prevent recursive logging calls
description: Avoid implementing logging calls that could trigger recursive logging
  patterns, which can lead to infinite loops and program crashes. This is particularly
  important in logging handlers, exporters, and instrumentation code.
repository: open-telemetry/opentelemetry-python
label: Logging
language: Python
comments_count: 4
repository_stars: 2061
---

Avoid implementing logging calls that could trigger recursive logging patterns, which can lead to infinite loops and program crashes. This is particularly important in logging handlers, exporters, and instrumentation code.

Key guidelines:
1. Use warnings.warn() instead of logging.log() in logging-sensitive code paths
2. Add clear comments warning about potential recursion risks
3. Consider using context flags to prevent recursion

Example of safe logging implementation:
```python
# Do not add any logging.log statements to this function
# they can trigger recursive calls that crash the program
def emit(self, log_data):
    try:
        self._exporter.export((log_data,))
    except Exception:
        warnings.warn(f"Exception while exporting logs: {traceback.format_exc()}")
```

For logging handlers and processors, consider using suppression flags:
```python
from opentelemetry.context import attach, set_value

def emit(self):
    token = attach(set_value(_SUPPRESS_INSTRUMENTATION_KEY, True))
    try:
        # Logging code here
        pass
    finally:
        detach(token)
```