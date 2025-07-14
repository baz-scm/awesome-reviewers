---
title: Resource-aware programming patterns
description: 'When optimizing application performance, be mindful of system resource
  constraints and use appropriate patterns to handle different scenarios efficiently:'
repository: nodejs/node
label: Performance Optimization
language: Markdown
comments_count: 3
repository_stars: 112178
---

When optimizing application performance, be mindful of system resource constraints and use appropriate patterns to handle different scenarios efficiently:

1. **I/O operations**: Use streaming APIs for large files instead of loading entire files into memory. This avoids hitting internal constraints and reduces memory pressure.

```javascript
// Inefficient for large files - may hit 2 GiB limit
fs.readFile('large-file.txt', (err, data) => {
  // Process the entire file at once
});

// Better approach - process chunks incrementally
const stream = fs.createReadStream('large-file.txt');
stream.on('data', (chunk) => {
  // Process each chunk as it arrives
});
```

2. **Memory management**: Monitor memory usage metrics to identify potential issues. Watch for signs like rising `rss` values while `heapTotal` remains stable, which may indicate memory fragmentation or leaks.

3. **Buffering strategy**: For performance-critical I/O operations, implement proper buffering with explicit flush control. Handle system resource constraints like EAGAIN errors gracefully with appropriate backpressure or fallback mechanisms.

Addressing these resource constraints proactively will help your application maintain consistent performance under various load conditions and system states.