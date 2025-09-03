---
title: Optimize collection operations
description: When processing collections of data, choose efficient algorithms and
  data structures that minimize computational complexity. Use appropriate array methods
  (filter, find, map, reduce) and consider batching operations when possible.
repository: novuhq/novu
label: Algorithms
language: TSX
comments_count: 4
repository_stars: 37700
---

When processing collections of data, choose efficient algorithms and data structures that minimize computational complexity. Use appropriate array methods (filter, find, map, reduce) and consider batching operations when possible.

Key principles:
- Use `find()` for single item searches instead of filtering entire arrays
- Leverage `Map` for deduplication and fast lookups by key
- Batch operations when processing multiple items to reduce API calls or iterations
- Consider the scope and context when searching collections to limit search space

Example from the codebase:
```javascript
// Efficient: Use find() for single item lookup
const localVariable = scopedVariables.find((v) => v.name === prefix);

// Efficient: Use Map for deduplication
const baseVariables = Array.from(new Map([...jitVariables, ...variables].map((item) => [item.name, item])).values());

// Efficient: Batch operations instead of individual updates
const bulkUpdatePreferences = (preferences: Preference[]) => async (channels: ChannelPreference) => {
  await novu.preferences.bulkUpdate(
    preferences.map((el) => {
      const channelsToUpdate = Object.keys(channels)
        .filter((channel) => oldChannels.includes(channel))
        .reduce((acc, channel) => {
          acc[channel] = channels[channel];
          return acc;
        }, {});
      return { preference: el, channels: channelsToUpdate };
    })
  );
};
```

This approach reduces time complexity and improves performance, especially when dealing with large datasets or frequent operations.