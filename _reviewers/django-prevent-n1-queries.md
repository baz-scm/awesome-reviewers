---
title: Prevent N+1 queries
description: The N+1 query problem is one of the most common performance bottlenecks
  in Django applications. This occurs when you retrieve a list of objects and then
  access related objects for each one individually, causing an additional database
  query for each parent object.
repository: django/django
label: Database
language: Txt
comments_count: 4
repository_stars: 84182
---

The N+1 query problem is one of the most common performance bottlenecks in Django applications. This occurs when you retrieve a list of objects and then access related objects for each one individually, causing an additional database query for each parent object.

To prevent N+1 queries, follow these strategies in order of complexity:

1. **Start with `FETCH_PEERS` mode**: This is the simplest approach and should be your first consideration when optimizing queries.

```python
from django.db.models import fetch_mode, FETCH_PEERS

# Apply to a specific code block
with fetch_mode(FETCH_PEERS):
    articles = Article.objects.all()
    for article in articles:
        print(article.reporter)  # Fetches all reporters in one query

# Or set globally in an AppConfig
from django.apps import AppConfig
from django.db.models import set_default_fetch_mode, FETCH_PEERS

class MyAppConfig(AppConfig):
    name = 'myapp'
    def ready(self):
        set_default_fetch_mode(FETCH_PEERS)
```

2. **Use `select_related()` for forward ForeignKey relationships**:
```python
# Instead of this (causes N+1 queries):
for article in Article.objects.all():
    print(article.reporter.name)

# Do this (single query):
for article in Article.objects.select_related('reporter'):
    print(article.reporter.name)
```

3. **Use `prefetch_related()` for reverse or many-to-many relationships**:
```python
# Instead of this (causes N+1 queries):
for reporter in Reporter.objects.all():
    print([article.headline for article in reporter.article_set.all()])

# Do this (two queries):
for reporter in Reporter.objects.prefetch_related('article_set'):
    print([article.headline for article in reporter.article_set.all()])
```

4. **For complex cases, combine approaches**:
```python
queryset = Book.objects.select_related('publisher').prefetch_related('authors')
```

5. **Use the `RAISE` fetch mode during development to catch accidental N+1 queries**:
```python
with fetch_mode(RAISE):
    # Code that should not trigger additional queries
    render(request, "template.html", context)
```

Remember that fetching too much data can also be inefficient. Choose the appropriate strategy based on your specific access patterns.