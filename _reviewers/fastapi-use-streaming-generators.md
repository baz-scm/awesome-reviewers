---
title: Use streaming generators
description: When processing large files or datasets, implement generator functions
  that yield data incrementally rather than loading everything into memory at once.
  This approach significantly improves memory efficiency and enables handling of arbitrarily
  large datasets that wouldn't fit in memory.
repository: fastapi/fastapi
label: Algorithms
language: Markdown
comments_count: 2
repository_stars: 86871
---

When processing large files or datasets, implement generator functions that yield data incrementally rather than loading everything into memory at once. This approach significantly improves memory efficiency and enables handling of arbitrarily large datasets that wouldn't fit in memory.

```python
def stream_file(filename):
    # Use a context manager to ensure the file is properly closed
    with open(filename, "rb") as file_like:
        # Yield from delegates iteration to the file object
        # Each chunk is yielded without loading the entire file
        yield from file_like
        
# Usage with FastAPI streaming response
@app.get("/large-file/")
def get_large_file():
    generator = stream_file("large_video.mp4")
    return StreamingResponse(generator, media_type="video/mp4")
```

Benefits of this pattern:
- Constant memory usage regardless of file size
- Immediate first byte to client response time
- Works well with asynchronous frameworks
- Compatible with cloud storage and remote data sources

For optimal performance, carefully choose appropriate chunk sizes when implementing custom generators. Too small chunks can create unnecessary overhead, while too large chunks defeat the purpose of streaming.