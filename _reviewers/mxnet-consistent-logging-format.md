---
title: Consistent logging format
description: Use consistent string formatting in logging statements throughout the
  codebase. Prefer `%` style placeholders over f-strings or `.format()` in logging
  calls as this is more efficient when logs are filtered by level (placeholders are
  only evaluated if the log is actually emitted).
repository: apache/mxnet
label: Logging
language: Python
comments_count: 3
repository_stars: 20801
---

Use consistent string formatting in logging statements throughout the codebase. Prefer `%` style placeholders over f-strings or `.format()` in logging calls as this is more efficient when logs are filtered by level (placeholders are only evaluated if the log is actually emitted).

For good logging practices:

1. Use placeholder style consistently:
```python
# Recommended
logging.info('%s benchmark running.', operation_type)

# Avoid mixing styles in the same codebase
logging.error('No models found in S3 bucket: {}'.format(bucket_name))
logging.warning(f'Failed to process {item_name}') # Avoid f-strings in logging
```

2. Reduce duplicate logging logic:
```python
# Instead of:
if opt.train:
    logging.info('%s training benchmark.', cell)
else:
    logging.info('%s inference benchmark.', cell)

# Prefer:
mode = 'training' if opt.train else 'inference'
logging.info('%s %s benchmark.', cell, mode)
```

3. Choose appropriate log levels based on severity:
   - Use `logging.error()` for failures that prevent normal operation
   - Use `logging.warning()` for potential issues that don't stop execution
   - Use assertions only for developer-facing invariants that should never be violated
   - Consider warnings instead of assertions in user-facing code
