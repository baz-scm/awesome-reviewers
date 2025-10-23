---
title: validate external system inputs
description: When integrating with external systems that receive repository or organizational
  information, always implement server-side validation to ensure the provided data
  belongs to authorized organizations or repositories. This prevents potential abuse
  where attackers could exploit organizational resources by spoofing repository information.
repository: servo/servo
label: Security
language: Yaml
comments_count: 1
repository_stars: 32962
---

When integrating with external systems that receive repository or organizational information, always implement server-side validation to ensure the provided data belongs to authorized organizations or repositories. This prevents potential abuse where attackers could exploit organizational resources by spoofing repository information.

The receiving system should validate that repository names, organization identifiers, or similar contextual data are constrained to expected values before processing requests or allocating resources.

Example from CI runner integration:
```yaml
# Action passes repository info to external monitor
echo "qualified_repo=${{ github.repository }}" | tee -a "$artifact_path"
```

The external monitor should validate that `github.repository` belongs to the authorized organization (e.g., "servo/*") before proceeding with runner allocation or resource provisioning. Without this validation, malicious actors could potentially abuse organizational infrastructure by providing crafted repository information.