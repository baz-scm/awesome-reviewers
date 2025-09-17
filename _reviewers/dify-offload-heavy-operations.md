---
title: Offload heavy operations
description: Move heavy operations, especially those involving large data processing
  or bulk deletions, from synchronous request handlers to asynchronous Celery tasks.
  This prevents request timeouts, improves user experience, and allows for better
  resource management.
repository: langgenius/dify
label: Celery
language: Python
comments_count: 2
repository_stars: 114231
---

Move heavy operations, especially those involving large data processing or bulk deletions, from synchronous request handlers to asynchronous Celery tasks. This prevents request timeouts, improves user experience, and allows for better resource management.

Heavy operations should be identified by their potential to:
- Process large amounts of data
- Perform bulk database operations (deletions, updates)
- Take significant time to complete
- Block request threads

Example implementation:
```python
# Instead of handling deletion directly in the controller
@setup_required
@login_required
def delete(self, app_model):
    # Move this to service layer with Celery
    pass

# Use Celery task in service layer
@classmethod
def delete(cls, app_model: App, conversation_id: str, user: Optional[Union[Account, EndUser]]):
    # Verify permissions first
    conversation = cls.get_conversation_for_deletion(app_model, conversation_id, user)
    
    # Queue the heavy deletion work as a Celery task
    delete_conversation_task.delay(conversation.id)
```

This pattern ensures that web requests remain responsive while heavy operations are processed in the background by Celery workers.