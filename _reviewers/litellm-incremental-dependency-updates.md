---
title: Incremental dependency updates
description: When updating dependencies in configuration files like requirements.txt,
  break large changes into smaller, focused pull requests that can be individually
  tested and validated. Each dependency update should include clear justification
  for why the change is necessary, especially when it triggers cascading updates to
  other packages.
repository: BerriAI/litellm
label: Configurations
language: Txt
comments_count: 2
repository_stars: 28310
---

When updating dependencies in configuration files like requirements.txt, break large changes into smaller, focused pull requests that can be individually tested and validated. Each dependency update should include clear justification for why the change is necessary, especially when it triggers cascading updates to other packages.

Before proposing dependency bumps, verify they are actually required by attempting to revert the changes and running the full test suite. If tests pass without the update, consider whether the dependency change is truly needed.

For example, when updating multiple packages:
```
# Instead of updating all at once:
# openai==1.40.0 -> 1.45.0
# google-cloud-aiplatform==1.50.0 -> 1.61.0  
# protobuf==4.25.0 -> 5.0.0

# Break into separate PRs:
# PR 1: Update openai to 1.45.0
# PR 2: Update protobuf to 5.0.0 (with justification)
# PR 3: Update google-cloud-aiplatform to 1.61.0 (if still needed)
```

This approach allows load testing and CI/CD validation of each change independently, making it easier to identify which specific update might cause issues and reducing the blast radius of potential problems.