---
title: Handle errors gracefully always
description: Always implement graceful error handling for resource lookups, data parsing,
  and system operations. Catch specific exceptions, provide clear error messages,
  and ensure the system can continue operating in a degraded state rather than failing
  completely.
repository: appwrite/appwrite
label: Error Handling
language: PHP
comments_count: 10
repository_stars: 51959
---

Always implement graceful error handling for resource lookups, data parsing, and system operations. Catch specific exceptions, provide clear error messages, and ensure the system can continue operating in a degraded state rather than failing completely.

Key practices:
1. Wrap resource lookups in try/catch blocks
2. Handle parsing errors explicitly
3. Provide fallback behavior
4. Use clear error messages

Example:
```php
try {
    $data = json_decode($input, true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        throw new Exception(Exception::GENERAL_BAD_REQUEST, 'Invalid JSON input');
    }
    
    $document = Authorization::skip(
        fn() => $dbForProject->getDocument('collection', $id)
    );
    
    if ($document->isEmpty()) {
        // Graceful degradation - use empty document
        $document = new Document();
        Console::warning("Document {$id} not found - using empty document");
    }
} catch (Throwable $e) {
    // Log error for debugging
    Console::error("Failed to process document {$id}: {$e->getMessage()}");
    // Return safe fallback state
    return new Document();
}
```

This approach ensures that:
- Resource lookups don't crash the application
- Data parsing errors are caught early with clear messages
- The system can continue operating even when components fail
- Errors are logged for debugging while maintaining stability