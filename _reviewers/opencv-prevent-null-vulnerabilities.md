---
title: Prevent null vulnerabilities
description: 'Use container classes and smart pointers instead of manual memory allocation
  to prevent null pointer dereferences and memory leaks.


  **Instead of raw memory allocation:**'
repository: opencv/opencv
label: Null Handling
language: C++
comments_count: 6
repository_stars: 82865
---

Use container classes and smart pointers instead of manual memory allocation to prevent null pointer dereferences and memory leaks.

**Instead of raw memory allocation:**
```cpp
// Problematic: Potential memory leak if exceptions occur
uint32_t* buffer = new uint32_t[size];
// ... operations that might throw
delete[] buffer;  // May never be reached
```

**Prefer container classes:**
```cpp
// Better: Automatic cleanup even with exceptions
std::vector<uint32_t> buffer(size);
// or
cv::AutoBuffer<uint32_t> buffer(size);  // May use stack space for small allocations
```

**For custom resource types, use smart pointers with appropriate deleters:**
```cpp
// Problematic: Manual resource management
WebPAnimDecoder* decoder = WebPAnimDecoderNew(&webp_data, &dec_options);
// ... operations
WebPAnimDecoderDelete(decoder);  // May be forgotten or skipped due to early returns

// Better: Automatic cleanup with custom deleter
struct UniquePtrDeleter {
    void operator()(WebPAnimDecoder* decoder) const { WebPAnimDecoderDelete(decoder); }
};
std::unique_ptr<WebPAnimDecoder, UniquePtrDeleter> decoder(WebPAnimDecoderNew(&webp_data, &dec_options));
```

**When null is invalid, use references instead of pointers:**
```cpp
// Problematic: Needs null check
uint32_t read_chunk(CHUNK* pChunk);

// Better: NULL is not possible
uint32_t read_chunk(CHUNK& pChunk);
```

Proper memory management not only prevents memory leaks but also eliminates many null pointer scenarios, making your code more robust and easier to maintain.
