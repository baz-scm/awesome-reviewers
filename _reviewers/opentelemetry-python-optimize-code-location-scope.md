---
title: Optimize code location scope
description: 'Place code in the most specific and appropriate location to improve
  findability and maintainability. Follow these principles:


  1. Avoid generic utility modules - place code in specific, relevant modules'
repository: open-telemetry/opentelemetry-python
label: Code Style
language: Python
comments_count: 7
repository_stars: 2061
---

Place code in the most specific and appropriate location to improve findability and maintainability. Follow these principles:

1. Avoid generic utility modules - place code in specific, relevant modules
2. Keep functions in the most specific scope possible
3. Extract repeated logic into dedicated functions
4. Split large files into focused modules
5. Prefer module-level functions over static methods when no instance state is needed

Example - Instead of:
```python
# generic util.py
def sanitize(key): ...

class CustomCollector:
    def _translate_to_prometheus(self, metric_record):
        # using global sanitize function
        label_keys.append(sanitize(label_key))
```

Better approach:
```python
# prometheus_translator.py
class CustomCollector:
    def _translate_to_prometheus(self, metric_record):
        def sanitize(key):  # Function in most specific scope
            # sanitization logic
            pass
            
        label_keys.append(sanitize(label_key))
```

This organization improves code findability, reduces coupling, and makes the codebase more maintainable.