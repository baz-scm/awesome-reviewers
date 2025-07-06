---
title: Strategic error handling
description: 'Choose appropriate error handling strategies based on the nature of
  the error and recovery potential:


  1. **Raise exceptions only for truly exceptional conditions**:'
repository: bridgecrewio/checkov
label: Error Handling
language: Python
comments_count: 5
repository_stars: 7667
---

Choose appropriate error handling strategies based on the nature of the error and recovery potential:

1. **Raise exceptions only for truly exceptional conditions**:
   - Use exceptions for invalid states that indicate logic errors or when recovery is impossible
   - For recoverable errors, consider returning default values or graceful fallbacks

```python
# Instead of always raising exceptions:
def get_sso_prismacloud_url(self, report_url: str) -> str:
    request = self.http.request("GET", url_saml_config, headers=headers, timeout=10)
    if request.status >= 300:
        # Return a fallback value instead of raising an exception
        return report_url
    # Normal processing continues...
```

2. **Implement appropriate recovery mechanisms**:
   - For transient errors (e.g., network issues), implement retries
   - For permanent errors, provide graceful degradation

```python
# Retry for transient errors:
for i in range(retries):
    request = self.http.request("POST", f"{self.prisma_api_url}/login", 
                              body=json.dumps({"username": username, "password": password}),
                              headers=headers)
    
    if request.status == 200:
        return json.loads(request.data.decode("utf8"))['token']
    elif request.status >= 500:  # Server errors are transient and should be retried
        continue
    elif request.status in [401, 403]:  # Authentication errors won't be resolved by retrying
        self.raise_bridgecrew_auth_error(request.status, request.data)
```

3. **Catch specific exceptions** rather than using broad exception handlers:

```python
try:
    module_name_index = len(full_definition_path) - full_definition_path[::-1][1:].index(BlockType.MODULE) - 1
except ValueError as e:
    # Handle the specific error case
    logging.warning(f"Could not determine module name index: {str(e)}")
# Instead of using a generic "except Exception" which catches everything
```

4. **Make deliberate decisions** about when to log errors versus raising exceptions:
   - Raise exceptions for conditions that indicate developer errors
   - Log and recover for operational issues that might resolve themselves

Following these principles leads to more robust code that fails gracefully when possible and provides clear error information when necessary.