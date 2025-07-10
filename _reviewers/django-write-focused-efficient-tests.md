---
title: Write focused efficient tests
description: 'Tests should be focused, efficient and meaningful. Follow these guidelines:


  1. Avoid testing implementation details or already-tested functionality

  2. Use clear, direct assertions that test actual behavior'
repository: django/django
label: Testing
language: Python
comments_count: 6
repository_stars: 84182
---

Tests should be focused, efficient and meaningful. Follow these guidelines:

1. Avoid testing implementation details or already-tested functionality
2. Use clear, direct assertions that test actual behavior
3. Prefer simple class-based tracking over complex mocks
4. Keep tests fast by avoiding unnecessary test cases

Example of a good test:
```python
def test_bulk_create_with_existing_children(self):
    """
    bulk_create() should continue _order sequence from existing children.
    """
    question = Question.objects.create(text="Test Question")
    Answer.objects.create(question=question, text="Existing 1")
    Answer.objects.create(question=question, text="Existing 2")

    new_answers = [
        Answer(question=question, text=f"New Answer {i}") 
        for i in range(2)
    ]
    created_answers = Answer.objects.bulk_create(new_answers)

    # Clear assertions testing actual behavior
    self.assertEqual(len(created_answers), 2)
    self.assertEqual(created_answers[0]._order, 2)
    self.assertEqual(created_answers[1]._order, 3)
```

This test is focused on specific functionality, uses clear assertions, and avoids unnecessary complexity while still thoroughly testing the behavior.