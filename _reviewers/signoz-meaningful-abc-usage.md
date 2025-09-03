---
title: meaningful ABC usage
description: Only inherit from ABC when you have abstract methods that subclasses
  must implement. Avoid using ABC inheritance for classes that don't define any abstract
  methods, as this adds unnecessary complexity without providing the intended benefits
  of the abstract base class pattern.
repository: SigNoz/signoz
label: Code Style
language: Python
comments_count: 2
repository_stars: 23369
---

Only inherit from ABC when you have abstract methods that subclasses must implement. Avoid using ABC inheritance for classes that don't define any abstract methods, as this adds unnecessary complexity without providing the intended benefits of the abstract base class pattern.

When you do use ABC, design it properly by defining abstract methods that enforce a contract for subclasses. This creates a clear interface that subclasses must follow.

Example of unnecessary ABC usage:
```python
from abc import ABC

class LogsResource(ABC):  # Unnecessary - no abstract methods
    def __init__(self, labels: dict[str, str]):
        self.labels = labels
    
    def np_arr(self) -> np.array:
        return np.array([self.labels])
```

Better approach - either remove ABC or add abstract methods:
```python
from abc import ABC, abstractmethod

class LogsResource(ABC):
    def __init__(self, labels: dict[str, str]):
        self.labels = labels
    
    @abstractmethod
    def np_arr(self) -> np.array:
        pass
    
    @abstractmethod
    def db_method(self):
        pass
```

This ensures that ABC inheritance serves its intended purpose of enforcing implementation contracts rather than adding unnecessary abstraction layers.