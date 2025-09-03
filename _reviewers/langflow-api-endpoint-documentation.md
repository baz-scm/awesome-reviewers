---
title: API endpoint documentation
description: Ensure API documentation includes all required networking components
  and uses proper syntax for shell commands. API examples must include authentication
  headers, use correct variable expansion syntax, and clearly state network configuration
  assumptions.
repository: langflow-ai/langflow
label: Networking
language: Markdown
comments_count: 3
repository_stars: 111046
---

Ensure API documentation includes all required networking components and uses proper syntax for shell commands. API examples must include authentication headers, use correct variable expansion syntax, and clearly state network configuration assumptions.

Key requirements:
- Include all required headers (especially authentication tokens like `x-api-key`)
- Use double quotes for shell commands containing variables to enable proper expansion
- Specify default network addresses and note when they might need modification
- Provide clear verification steps for network connectivity

Example of proper curl documentation:
```bash
curl -X POST "http://localhost:7860/api/v1/run/$FLOW_ID" \
-H "Content-Type: application/json" \
-H "x-api-key: $LANGFLOW_API_KEY" \
-d '{
    "input_value": "message",
    "input_type": "chat",
    "output_type": "chat"
}'
```

This ensures developers can successfully integrate with network services without encountering authentication failures or variable expansion issues that would prevent proper API communication.