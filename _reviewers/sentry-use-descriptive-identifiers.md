---
title: Use descriptive identifiers
description: Choose variable, parameter, field, and class names that clearly communicate
  their purpose and context. Favor specific, self-explanatory identifiers over generic
  or ambiguous ones, and ensure they follow Python's snake_case convention.
repository: getsentry/sentry
label: Naming Conventions
language: Python
comments_count: 6
repository_stars: 41297
---

Choose variable, parameter, field, and class names that clearly communicate their purpose and context. Favor specific, self-explanatory identifiers over generic or ambiguous ones, and ensure they follow Python's snake_case convention.

When naming variables:
1. Avoid generic names like `func`, `type_str`, or `dict1` that don't explain their purpose
2. Include qualifying context when similar names exist elsewhere in the codebase
3. Make names reflect the entity's primary behavior or responsibility

Bad:
```python
def serialize_rpc_event(self, event, group_cache, additional_attributes):
    attributeDict = {
        attribute: event[attribute] 
        for attribute in additional_attributes
        if attribute in event
    }
    
def _assemble_preprod_artifact(assemble_task, project_id, org_id, checksum, chunks, func):
    # func is too generic and unclear what type of function is expected
```

Good:
```python
def serialize_rpc_event(self, event, group_cache, additional_attributes):
    attribute_dict = {
        attribute: event[attribute] 
        for attribute in additional_attributes
        if attribute in event
    }
    
def _assemble_preprod_artifact(assemble_task, project_id, org_id, checksum, chunks, callback):
    # callback clearly indicates the expected function's purpose
```

For class naming, ensure the name reflects the primary purpose:
```python
# Instead of MultiProducerManager for a class that mainly acts as a producer
class MultiProducer:
    def produce(self):
        # implementation
```

When related but distinct concepts exist, use clear differentiators in names:
```python
# Instead of ambiguous:
data_source_id = data_packet.source_id

# Use more specific naming:
data_packet_source_id = data_packet.source_id  # Avoids confusion with DataSource.id
```