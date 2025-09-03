---
title: API authentication requirements
description: Ensure all API documentation and code examples include proper authentication
  headers and clearly explain authentication requirements. As of Langflow v1.5, all
  API requests require a Langflow API key, even when `AUTO_LOGIN` is enabled. The
  only exceptions are MCP endpoints (`/v1/mcp`, `/v1/mcp-projects`, `/v2/mcp`) which
  don't require authentication...
repository: langflow-ai/langflow
label: API
language: Markdown
comments_count: 19
repository_stars: 111046
---

Ensure all API documentation and code examples include proper authentication headers and clearly explain authentication requirements. As of Langflow v1.5, all API requests require a Langflow API key, even when `AUTO_LOGIN` is enabled. The only exceptions are MCP endpoints (`/v1/mcp`, `/v1/mcp-projects`, `/v2/mcp`) which don't require authentication regardless of the `AUTO_LOGIN` setting.

All curl examples, code snippets, and API documentation should include the `x-api-key` header:

```bash
curl -X POST \
  "http://localhost:7860/api/v1/run/FLOW_ID" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $LANGFLOW_API_KEY" \
  -d '{"input_value": "Hello"}'
```

When documenting API endpoints, explicitly state authentication requirements and provide guidance on obtaining API keys. Update any legacy examples that assume no authentication is needed, and ensure consistency across all API-related documentation. This prevents user confusion and ensures examples work out of the box with current Langflow versions.