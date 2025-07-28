---
title: Cache correctness validation
description: Ensure caching implementations store the correct data and use appropriate
  strategies for the context. Cache should store the final processed output, not intermediate
  or input data, and should include strategy options for different security/performance
  requirements.
repository: prettier/prettier
label: Caching
language: JavaScript
comments_count: 4
repository_stars: 50772
---

Ensure caching implementations store the correct data and use appropriate strategies for the context. Cache should store the final processed output, not intermediate or input data, and should include strategy options for different security/performance requirements.

Key considerations:
- **Store processed output**: Cache the formatted result, not the original input. When using `--write` flag, cache the formatted content, not the unformatted input.
- **Provide strategy options**: Implement both metadata-based (faster) and content-based (more secure) caching strategies, similar to ESLint's `--cache-strategy` option.
- **Handle format changes gracefully**: When cache format changes between versions, detect incompatible formats and recreate the cache rather than throwing errors.
- **Validate cache usage context**: Ensure cache is not used inappropriately (e.g., don't cache stdin input, verify cache matches current options).

Example implementation:
```javascript
// Good: Store formatted output and handle strategy
if (isCacheExists && cacheStrategy === "content") {
  result = { formatted: input };
} else {
  result = format(context, input, options);
  // Cache the formatted result, not the input
  formatResultsCache?.setFormatResultsCache(filename, result.formatted, options);
}

// Good: Handle cache format changes
try {
  this.#fileEntryCache = fileEntryCache.createFromFile(cacheFileLocation, useChecksum);
} catch {
  // If cache format changed, delete and retry
  fs.unlinkSync(cacheFileLocation);
  this.#fileEntryCache = fileEntryCache.createFromFile(cacheFileLocation, useChecksum);
}
```

This ensures cache reliability and prevents subtle bugs where cached data doesn't match expected output.