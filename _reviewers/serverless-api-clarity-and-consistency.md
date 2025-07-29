---
title: API clarity and consistency
description: Ensure API configurations, documentation, and terminology are clear,
  consistent, and properly organized. Group related API properties together logically,
  use precise terminology that matches the underlying service (e.g., distinguish "HTTP
  API" from "REST API"), and maintain consistent naming conventions throughout.
repository: serverless/serverless
label: API
language: Markdown
comments_count: 5
repository_stars: 46810
---

Ensure API configurations, documentation, and terminology are clear, consistent, and properly organized. Group related API properties together logically, use precise terminology that matches the underlying service (e.g., distinguish "HTTP API" from "REST API"), and maintain consistent naming conventions throughout.

When organizing API configurations, group related properties under logical sections and order them by usage frequency to improve discoverability. Use naming conventions that align with the underlying service's terminology.

Example of good API configuration organization:
```yml
provider:
  apiGateway:
    # More commonly used, placed first
    restApiId: existing-api-id
  websockets:
    # Grouped together logically
    apiName: custom-websockets-api-name
    apiRouteSelectionExpression: $request.body.route
    description: Custom Serverless Websockets
```

In documentation, use precise API terminology and provide clear context for examples. Avoid generic terms when specific ones exist, and ensure examples include sufficient context to understand their purpose and application.