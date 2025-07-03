---
title: Structure for navigation
description: 'Documentation should be structured to optimize user navigation and information
  discovery. When organizing documentation elements:


  1. Group related information into logical categories to help users find relevant
  content faster'
repository: kubeflow/kubeflow
label: Documentation
language: Yaml
comments_count: 2
repository_stars: 15064
---

Documentation should be structured to optimize user navigation and information discovery. When organizing documentation elements:

1. Group related information into logical categories to help users find relevant content faster
2. Maintain consistent formatting and width across similar elements for better readability
3. Consider user scanning patterns - users often skim content, so key information should be easily visible
4. Use alphabetical sorting within groups to create predictable navigation patterns

For example, when creating documentation indexes or navigation elements:

```yaml
# Good organization example
documentation_links:
  # Community resources (general info)
  - name: Documentation
    url: https://docs.example.org/
    about: Official Documentation
    
  - name: Community Support
    url: https://community.example.org/
    about: Get help from the community
    
  # Component-specific resources (alphabetically sorted)
  - name: API Reference
    url: https://api.example.org/
    about: Please refer to the API documentation
    
  - name: Installation Guide
    url: https://install.example.org/
    about: Follow the installation steps
```

This organization style makes navigation intuitive and ensures users can quickly find the information they need, rather than getting lost in poorly structured documentation.
