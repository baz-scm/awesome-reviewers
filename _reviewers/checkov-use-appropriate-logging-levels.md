---
title: Use appropriate logging levels
description: 'Select the correct logging level based on the message''s importance
  and intended audience:


  - Use `logging.ERROR` for critical failures requiring immediate attention'
repository: bridgecrewio/checkov
label: Logging
language: Python
comments_count: 6
repository_stars: 7667
---

Select the correct logging level based on the message's importance and intended audience:

- Use `logging.ERROR` for critical failures requiring immediate attention
- Use `logging.WARNING` for unusual situations that might indicate problems but don't break functionality
- Use `logging.INFO` for significant operational events and normal application flow
- Use `logging.DEBUG` for detailed information useful during development and troubleshooting

This helps with log filtering and ensures important messages aren't lost in noise. Additionally:
- Include clear context in log messages to aid troubleshooting
- Use consistent formatting for similar types of messages
- Prefer logging over print statements for better control and integration

Example:
```python
# Too verbose for regular operation
logging.debug(f"OpenAI request returned: {completion}")  

# Important operational metrics
logging.info(f"Done persisting {len(resource_subgraph_maps)} resource_subgraph_maps")

# Abnormal but non-critical situations
logging.warning(f"Cant find address: {address} in tf graph")

# Instead of print statements
logging.info(f"Error while calling Prisma Cloud API: {e}")  # Not: print(f"Error...")
```