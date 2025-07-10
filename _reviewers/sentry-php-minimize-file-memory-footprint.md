---
title: Minimize file memory footprint
description: 'When handling files in your application, minimize memory usage to optimize
  performance. Follow these guidelines:


  1. **Avoid multiple reads**: Read file content only once and reuse it throughout
  your code. Each read operation loads the entire file into memory.'
repository: getsentry/sentry-php
label: Performance Optimization
language: PHP
comments_count: 3
repository_stars: 1873
---

When handling files in your application, minimize memory usage to optimize performance. Follow these guidelines:

1. **Avoid multiple reads**: Read file content only once and reuse it throughout your code. Each read operation loads the entire file into memory.

2. **Use metadata functions**: When you only need file information (not content), use metadata functions like `filesize()` instead of reading the file.

3. **Consider streaming**: For large files, use stream operations instead of loading the entire content into memory.

Example refactoring:

```php
// Before: Inefficient - reads file twice and holds it twice in memory
public static function fromFile(string $filename, string $contentType): self
{
    $data = file_get_contents($filename); // First read
    
    $attachmentItemHeader = [
        'type' => 'attachment',
        'filename' => $filename,
        'content_type' => $contentType,
        'length' => strlen($data), // Requires second read or keeping in memory
    ];
    
    return new self($data, $filename, $contentType);
}

// After: Efficient - reads file once, uses filesize() for metadata
public static function fromFile(string $filename, string $contentType): self
{
    // Use metadata function instead of reading content
    $fileLength = filesize($filename);
    
    $attachmentItemHeader = [
        'type' => 'attachment',
        'filename' => $filename, 
        'content_type' => $contentType,
        'length' => $fileLength, // No need to read content for length
    ];
    
    // Read content only when needed
    $data = file_get_contents($filename);
    return new self($data, $filename, $contentType);
}
```

For very large files, consider using stream operations to process the file incrementally rather than loading it entirely into memory.