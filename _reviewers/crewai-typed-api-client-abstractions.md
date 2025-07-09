---
title: Typed API client abstractions
description: When designing API clients, encapsulate responses in typed objects rather
  than passing raw JSON throughout your codebase. This improves maintainability, enables
  better error handling, and provides type safety.
repository: crewaiinc/crewai
label: API
language: Python
comments_count: 3
repository_stars: 33945
---

When designing API clients, encapsulate responses in typed objects rather than passing raw JSON throughout your codebase. This improves maintainability, enables better error handling, and provides type safety.

For HTTP API clients, use session objects to handle common configurations like authentication headers and base URLs. This approach reduces code duplication and creates a cleaner interface.

Example:

```python
# Instead of this:
def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
    url = f"{self.base_url}/{endpoint}"
    return requests.request(method, url, headers=self.headers, **kwargs)

# Do this:
class CrewAPI:
    def __init__(self, api_key: str) -> None:
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
        self.base_url = "https://api.example.com/v2"
        
    def deploy_by_name(self, project_name: str) -> DeployResponse:
        """Deploy a project by name and return a typed response."""
        url = f"{self.base_url}/deploy/{project_name}"
        response = self.session.post(url)
        
        if not response.ok:
            raise APIError(response.json())
            
        return DeployResponse.from_json(response.json())
        
class DeployResponse:
    """Typed representation of a deployment response."""
    uuid: str
    status: str
    timestamp: datetime
    
    @classmethod
    def from_json(cls, data: dict) -> 'DeployResponse':
        # Convert raw JSON to typed object
        return cls(**data)
```

This pattern ensures that API-specific concerns stay in the client implementation while providing a clean, type-safe interface for consumers.