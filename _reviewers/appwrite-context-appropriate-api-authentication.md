---
title: Context-appropriate API authentication
description: Always use the authentication method appropriate for your API client's
  execution context. Server-side SDKs should use API key authentication (with `setKey()`)
  rather than session-based authentication, which is meant for client-side applications.
repository: appwrite/appwrite
label: API
language: Markdown
comments_count: 2
repository_stars: 51959
---

Always use the authentication method appropriate for your API client's execution context. Server-side SDKs should use API key authentication (with `setKey()`) rather than session-based authentication, which is meant for client-side applications.

**Why it matters:**
- Server SDKs are designed to work with API keys for secure backend operations
- Session-based authentication (`setSession()`) won't function properly in server contexts
- Consistent authentication patterns improve maintainability across projects

**Example - PHP Server SDK:**
```php
$client = (new Client())
    ->setEndpoint('https://<REGION>.cloud.appwrite.io/v1') 
    ->setProject('<YOUR_PROJECT_ID>')
    ->setKey('<YOUR_API_KEY>'); // Correct: Using API key for server authentication
    // ->setSession(''); // Incorrect: Session auth doesn't work server-side
```

**Example - Kotlin Server SDK:**
```kotlin
val client = Client()
    .setEndpoint("https://<REGION>.cloud.appwrite.io/v1")
    .setProject("<YOUR_PROJECT_ID>")
    .setKey("<YOUR_API_KEY>") // Correct: Using API key for server authentication
    // .setSession("") // Incorrect: Session auth doesn't work server-side
```