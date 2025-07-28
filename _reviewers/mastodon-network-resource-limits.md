---
title: Network resource limits
description: Implement protective limits for network operations to prevent resource
  exhaustion and denial-of-service attacks. Network operations should have bounded
  resource consumption to avoid overwhelming servers or clients.
repository: mastodon/mastodon
label: Networking
language: Ruby
comments_count: 3
repository_stars: 48691
---

Implement protective limits for network operations to prevent resource exhaustion and denial-of-service attacks. Network operations should have bounded resource consumption to avoid overwhelming servers or clients.

Key areas to address:

1. **Pagination limits**: Set maximum page counts and track visited pages to prevent infinite loops in collection traversal
2. **Connection management**: Consume response bodies within reasonable limits (e.g., 1MB) for persistent connections, closing connections when limits are exceeded
3. **Subscription churn**: Avoid creating excessive per-resource network channels that cause high subscribe/unsubscribe load

Example implementation for pagination protection:
```ruby
def collection_items(collection_or_uri)
  visited_pages = Set.new
  page_count = 0
  max_pages = 50
  
  while collection.is_a?(Hash) && page_count < max_pages
    return if visited_pages.include?(collection['id'])
    visited_pages.add(collection['id'])
    
    # Process items...
    page_count += 1
    collection = collection['next'].present? ? fetch_collection(collection['next']) : nil
  end
end
```

This prevents attackers from creating infinite pagination loops while ensuring legitimate large collections can still be processed within reasonable bounds.