---
title: Assert response fully always
description: Always validate all relevant aspects of API responses in tests, including
  status codes, headers, and body content. Don't partially validate responses or make
  assumptions about response structure.
repository: appwrite/appwrite
label: Testing
language: PHP
comments_count: 5
repository_stars: 51959
---

Always validate all relevant aspects of API responses in tests, including status codes, headers, and body content. Don't partially validate responses or make assumptions about response structure.

Example of incomplete testing:
```php
$response = $this->client->call(Method::POST, '/endpoint');
$this->assertNotEmpty($response['body']); // Too vague
```

Better approach with comprehensive validation:
```php
$response = $this->client->call(Method::POST, '/endpoint');
// Validate HTTP status
$this->assertEquals(201, $response['headers']['status-code']);

// Validate response structure
$this->assertIsArray($response['body']);
$this->assertArrayHasKey('id', $response['body']);

// Validate specific content
$this->assertEquals('expected-value', $response['body']['field']);
$this->assertGreaterThan(0, $response['body']['count']);
```

Key points:
1. Always assert HTTP status codes
2. Validate response structure before checking content
3. Include both positive and negative assertions
4. Test edge cases and error conditions
5. Verify all relevant response fields, not just the "happy path"