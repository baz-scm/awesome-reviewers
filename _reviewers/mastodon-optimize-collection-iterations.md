---
title: optimize collection iterations
description: Avoid multiple passes through the same data structure when a single iteration
  can accomplish the same work. This reduces computational complexity and improves
  performance, especially for large datasets.
repository: mastodon/mastodon
label: Algorithms
language: Ruby
comments_count: 3
repository_stars: 48691
---

Avoid multiple passes through the same data structure when a single iteration can accomplish the same work. This reduces computational complexity and improves performance, especially for large datasets.

Instead of using multiple array traversals like `filter_map` chains:

```ruby
# Inefficient: multiple traversals
params = uris.filter_map { |uri| uri_to_local_account_params(uri) }
usernames = params.filter_map { |param, value| value.downcase if param == :username }
ids = params.filter_map { |param, value| value if param == :id }
```

Use a single iteration to collect all needed data:

```ruby
# Efficient: single traversal
usernames = []
ids = []

uris.each do |uri|
  param, value = uri_to_local_account_params(uri)
  usernames << value.downcase if param == :username
  ids << value if param == :id
end
```

This principle also applies to avoiding duplicate iteration logic in collection processing services and preventing redundant recursive operations by checking if work has already been completed before proceeding.