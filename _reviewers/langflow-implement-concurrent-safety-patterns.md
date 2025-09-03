---
title: Implement concurrent safety patterns
description: When designing concurrent systems, implement comprehensive safety patterns
  that handle resource lifecycle management, race conditions, and proper cleanup mechanisms.
  This includes setting resource limits to prevent exhaustion, implementing timeout-based
  cleanup for idle resources, and handling database race conditions with proper rollback
  and retry logic.
repository: langflow-ai/langflow
label: Concurrency
language: Python
comments_count: 2
repository_stars: 111046
---

When designing concurrent systems, implement comprehensive safety patterns that handle resource lifecycle management, race conditions, and proper cleanup mechanisms. This includes setting resource limits to prevent exhaustion, implementing timeout-based cleanup for idle resources, and handling database race conditions with proper rollback and retry logic.

Key patterns to implement:

1. **Resource Lifecycle Management**: Use structured cleanup with limits and timeouts
```python
class ResourceManager:
    def __init__(self):
        self.resources_by_key = {}  # Group resources by identity
        self._cleanup_task = asyncio.create_task(self._periodic_cleanup())
    
    async def _periodic_cleanup(self):
        """Periodically clean up idle resources."""
        while True:
            await asyncio.sleep(CLEANUP_INTERVAL)
            await self._cleanup_idle_resources()
    
    async def get_resource(self, key, params):
        # Check limits before creating new resources
        if len(self.resources_by_key.get(key, {})) >= MAX_RESOURCES_PER_KEY:
            # Remove oldest resource
            await self._cleanup_oldest_resource(key)
```

2. **Race Condition Handling**: Implement proper exception handling with rollback and retry
```python
async def create_resource(name, session):
    try:
        # Check if resource exists
        existing = await get_resource_by_name(name, session)
        if existing:
            return existing
        
        # Create new resource
        resource = Resource(name=name)
        session.add(resource)
        await session.commit()
        return resource
    except IntegrityError:
        # Handle race condition - another worker created it
        await session.rollback()
        existing = await get_resource_by_name(name, session)
        if existing:
            return existing
        raise  # Re-raise if no resource found after rollback
```

3. **Test Concurrent Scenarios**: Use `asyncio.gather()` to test real concurrent behavior
```python
@pytest.mark.asyncio
async def test_concurrent_resource_creation():
    """Test multiple concurrent calls handle race conditions properly."""
    tasks = [
        create_resource("shared_name", session1),
        create_resource("shared_name", session2)
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    # Verify both succeed or handle conflicts gracefully
```

Always consider the impact of automatic resource cleanup on user experience and provide clear boundaries for resource limits to prevent unexpected behavior disruptions.