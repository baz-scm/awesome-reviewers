---
title: Environment-aware configuration design
description: Design configurations that work consistently across different environments
  without requiring environment-specific modifications. Configurations should be parameterized
  and adaptable to various deployment contexts (development, production, air-gapped
  environments).
repository: kubeflow/kubeflow
label: Configurations
language: Yaml
comments_count: 3
repository_stars: 15064
---

Design configurations that work consistently across different environments without requiring environment-specific modifications. Configurations should be parameterized and adaptable to various deployment contexts (development, production, air-gapped environments).

Key practices:
- Avoid hardcoding environment-specific values
- Parameterize configurations to accept values from environment variables
- Consider accessibility constraints (like air-gapped environments)
- Test configurations across different target environments

For example, instead of:
```yaml
# Only works in master branch with "latest" tag
export CURRENT_CENTRALDB_IMG=docker.io/kubeflownotebookswg/centraldashboard:latest
kustomize build overlays/kserve | kubectl apply -f -
```

Use a more flexible approach:
```yaml
# Works across different branches and environments
IMG=${{env.IMG}}:${{env.TAG}}
kustomize build overlays/kserve | kubectl apply -f -
kubectl patch deployment $DEPLOYMENT -n kubeflow --patch \
  '{"spec": {"template": {"spec": {"containers": [{"name": "'"$CONTAINER"'","image": "'"$IMG"'"}]}}}}'
```

Additionally, for UI resources, consider providing configuration options that work in restricted network environments:
```yaml
# Configurable options for different environments
imageOptions:
  - source: internal  # For air-gapped environments
  - source: external  # For internet-connected environments
```
