---
title: Optimize API consumption
description: 'When interacting with APIs, minimize network requests and improve code
  maintainability by:

  1. Extracting repetitive API call patterns into reusable functions'
repository: temporalio/temporal
label: API
language: Yaml
comments_count: 2
repository_stars: 14953
---

When interacting with APIs, minimize network requests and improve code maintainability by:
1. Extracting repetitive API call patterns into reusable functions
2. Retrieving multiple data points with a single API call when possible

Example:
```bash
# Create a reusable function for API calls
call() {
  curl -fL -X POST -H "Accept: application/vnd.github.v3+json" -H "Authorization: token $PAT" "$@"
}

# Use the function and make a single API call to get multiple pieces of data
result=$(call "https://api.github.com/repos/$PARENT_REPO/actions/runs/$run_id")
status=$(echo "$result" | jq -r .status)
conclusion=$(echo "$result" | jq -r .conclusion)
```