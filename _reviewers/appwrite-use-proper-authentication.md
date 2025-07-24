---
title: Use proper authentication
description: Always implement the correct authentication method for API clients as
  specified in the SDK documentation. Incorrect authentication methods can lead to
  security vulnerabilities, API access failures, or unintended behavior.
repository: appwrite/appwrite
label: Security
language: Markdown
comments_count: 1
repository_stars: 51959
---

Always implement the correct authentication method for API clients as specified in the SDK documentation. Incorrect authentication methods can lead to security vulnerabilities, API access failures, or unintended behavior.

**Incorrect example:**
```java
Client client = new Client()
    .setEndpoint("https://<REGION>.cloud.appwrite.io/v1")
    .setProject("<YOUR_PROJECT_ID>")
    .setSession(""); // INCORRECT: Empty session token
```

**Correct examples:**
```java
// For API key authentication (server-side)
Client client = new Client()
    .setEndpoint("https://<REGION>.cloud.appwrite.io/v1")
    .setProject("<YOUR_PROJECT_ID>")
    .setKey("<YOUR_API_KEY>");

// For JWT authentication
Client client = new Client()
    .setEndpoint("https://<REGION>.cloud.appwrite.io/v1")
    .setProject("<YOUR_PROJECT_ID>")
    .setJWT("<YOUR_JWT>");
```

Using the proper authentication method ensures your application interacts securely with external services and prevents unauthorized access.