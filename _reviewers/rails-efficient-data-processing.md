---
title: Efficient data processing
description: When implementing algorithms that process large data streams or collections,
  use a chunking approach rather than processing the entire input at once. This improves
  memory efficiency and prevents out-of-memory errors for large inputs.
repository: rails/rails
label: Algorithms
language: Ruby
comments_count: 4
repository_stars: 57027
---

When implementing algorithms that process large data streams or collections, use a chunking approach rather than processing the entire input at once. This improves memory efficiency and prevents out-of-memory errors for large inputs.

Key practices to follow:

1. Process data in manageable chunks when dealing with potentially large inputs
2. Be consistent in chunking strategy across related operations
3. Remember to properly initialize data structures that will grow during processing
4. Reset stream positions (e.g., rewind) after processing when the data needs to be reused

```ruby
# Efficient implementation with chunking
def compute_checksum_in_chunks(io, algorithm: default_algorithm)
  raise ArgumentError, "io must be rewindable" unless io.respond_to?(:rewind)
  
  digest = checksum_implementation(algorithm).new.tap do |checksum|
    read_buffer = "".b  # Binary string buffer for reuse
    while io.read(5.megabytes, read_buffer)  # Process in 5MB chunks
      checksum << read_buffer  # Update digest with each chunk
    end
    
    io.rewind  # Reset stream position for reuse
  end.base64digest
end

# Properly initialize a hash that will hold growing collections
@collection_map = Hash.new { |h, k| h[k] = {} }  # Each key gets its own hash
```

Always consider the memory implications of your algorithm implementation, especially when processing user-generated content of unpredictable size. Using chunked processing patterns helps ensure your code performs well at scale while maintaining consistent memory usage.
