---
title: Tests must assert
description: Test methods should contain active, uncommented code that includes at
  least one assertion to verify expected behavior. Commented-out test code provides
  zero value and creates a false sense of security by appearing to test functionality
  while actually testing nothing.
repository: continuedev/continue
label: Testing
language: Python
comments_count: 3
repository_stars: 27819
---

Test methods should contain active, uncommented code that includes at least one assertion to verify expected behavior. Commented-out test code provides zero value and creates a false sense of security by appearing to test functionality while actually testing nothing.

Instead of:
```python
def testGetResponse(self):
    # inst = self.make_instance(include_optional=False)
    # self.assertEqual(inst.message, "Expected message")
```

Write:
```python
def testGetResponse(self):
    inst = self.make_instance(include_optional=False)
    self.assertIsNotNone(inst)
    self.assertEqual(inst.message, "Expected message")
```

Every test method should verify specific functionality by executing the code under test and validating results through appropriate assertions. Tests without assertions or with only commented code will always pass regardless of code correctness, defeating the purpose of having tests.