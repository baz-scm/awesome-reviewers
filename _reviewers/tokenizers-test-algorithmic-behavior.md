---
title: Test algorithmic behavior
description: When testing algorithms, verify their actual functionality rather than
  just checking for proper instantiation or property modification. Ensure your tests
  capture the core behaviors of the algorithm under various parameters.
repository: huggingface/tokenizers
label: Algorithms
language: Python
comments_count: 2
repository_stars: 9868
---

When testing algorithms, verify their actual functionality rather than just checking for proper instantiation or property modification. Ensure your tests capture the core behaviors of the algorithm under various parameters.

For deterministic algorithms:
- Test with different input parameters and verify the expected output
- Include edge cases that might affect algorithm behavior

For non-deterministic algorithms:
- Focus on testing invariant properties rather than exact outputs
- Identify the stable parts of the output that should always be consistent

Example:
```python
# Insufficient test - only checks properties
def test_fixed_length_weak():
    pretok = FixedLength(length=5)
    assert pretok.length == 5
    
    pretok.length = 10
    assert pretok.length == 10

# Better test - verifies actual algorithm behavior
def test_fixed_length_complete():
    test_string = "This is a test string for tokenization"
    
    # Test with length=5
    pretok = FixedLength(length=5)
    output_5 = pretok.pre_tokenize(test_string)
    assert len(output_5[0]) == 5  # First chunk should be 5 chars
    assert "".join([t for t, _ in output_5]) == test_string  # Original text preserved
    
    # Test with length=10
    pretok.length = 10
    output_10 = pretok.pre_tokenize(test_string)
    assert len(output_10[0]) == 10  # First chunk should be 10 chars
    assert len(output_10) < len(output_5)  # Fewer chunks with larger length
```

For algorithms with inherent variability (like probabilistic models), focus on testing stable properties rather than specific outputs that might change between runs.