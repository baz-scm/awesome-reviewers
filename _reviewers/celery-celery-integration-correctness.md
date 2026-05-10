---
title: Celery Integration Correctness
description: 'Celery should only execute tasks when its assumptions about state and
  message format are guaranteed.


  Apply these rules:


  1) Django: trigger tasks after the DB commit'
repository: celery/celery
label: Celery
language: Other
comments_count: 2
repository_stars: 28464
---

Celery should only execute tasks when its assumptions about state and message format are guaranteed.

Apply these rules:

1) Django: trigger tasks after the DB commit
- Don’t call `send_email.delay(...)` (or similar) inside the request flow before the transaction is committed.
- Use `transaction.on_commit(...)` or Celery’s Django task integration.

Example (safe timing):

```python
# views.py
from django.db import transaction

def create_user(request):
    user = User.objects.create(username=request.POST['username'])
    transaction.on_commit(lambda: send_email.delay(user.pk))
    return HttpResponse('User created')
```

Optional Celery shortcut (Django task class):

```python
from celery import Celery

app = Celery('proj', task_cls='celery.contrib.django.task:Task')
```

2) Kafka (and other transports): configure required serializers precisely
- Ensure the task serializer is set to JSON when required.
- Don’t set or constrain `result_serializer` unless you actually need to.

Example:

```python
# celeryconfig.py
task_serializer = 'json'      # required
# result_serializer = ...     # only set if you have a need
```