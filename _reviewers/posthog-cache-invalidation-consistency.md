---
title: Cache invalidation consistency
description: Ensure comprehensive and consistent cache invalidation patterns across
  all models that affect cached data. Every model that can impact cached content must
  have proper invalidation signals, and cache keys should be designed to enable targeted
  busting without affecting unrelated data.
repository: PostHog/posthog
label: Caching
language: Python
comments_count: 6
repository_stars: 28460
---

Ensure comprehensive and consistent cache invalidation patterns across all models that affect cached data. Every model that can impact cached content must have proper invalidation signals, and cache keys should be designed to enable targeted busting without affecting unrelated data.

Key requirements:
1. **Complete signal coverage**: Add both `post_save` and `post_delete` receivers for all models that affect cached data, even if soft deletes are primarily used
2. **Consistent invalidation patterns**: Don't rely on developers to remember to add cache busting - make it systematic and hard to miss
3. **Targeted cache keys**: Use Redis hashes with structured keys like `team_id:git_sha:model_name` to enable selective invalidation without clearing unrelated cache entries
4. **Handle related model changes**: Consider how foreign key and many-to-many relationships affect cached data and ensure those changes also trigger appropriate invalidation

Example implementation:
```python
# Bad - easy to forget invalidation for new models
class ExternalDataSource(models.Model):
    objects: CacheManager = CacheManager()
    # Missing: no invalidation signals

# Good - systematic invalidation pattern
class ExternalDataSource(models.Model):
    objects: CacheManager = CacheManager()

@receiver(post_save, sender=ExternalDataSource)
@receiver(post_delete, sender=ExternalDataSource)  # Even with soft deletes
def invalidate_external_data_source_cache(sender, instance, **kwargs):
    ExternalDataSource.objects.invalidate_cache(instance.team_id)
```

This prevents the common issue where "ORM writes (including bulk updates, signals, admin edits, scripts) can bypass your invalidation path → stale cache" and ensures that cache invalidation is not an afterthought that developers can easily miss when adding new cached models.