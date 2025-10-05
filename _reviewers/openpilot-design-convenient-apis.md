---
title: Design convenient APIs
description: APIs should provide convenient methods that handle common operations
  directly, rather than requiring users to write helper functions or use verbose patterns.
  This improves developer experience and reduces boilerplate code.
repository: commaai/openpilot
label: API
language: Python
comments_count: 2
repository_stars: 58214
---

APIs should provide convenient methods that handle common operations directly, rather than requiring users to write helper functions or use verbose patterns. This improves developer experience and reduces boilerplate code.

Key principles:
- Build common functionality like type conversion into API methods themselves
- Provide simple, direct constructor patterns for object creation
- Avoid forcing users to chain multiple method calls for basic operations

Example of good API design:
```python
# Good: Simple constructor with direct parameter passing
CC = car.CarControl(cruiseControl={'cancel': True})

# Avoid: Verbose chaining that could be simplified
CC = car.CarControl.new_message(cruiseControl={'cancel': True})
test_car_controller(CC.as_reader())
```

When designing APIs, consider what the most common use cases will be and optimize the interface for those scenarios. If you find yourself writing helper functions or seeing users write repetitive boilerplate, that's a signal the API could be more convenient.