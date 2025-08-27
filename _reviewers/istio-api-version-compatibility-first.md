---
title: API version compatibility first
description: When selecting API versions, prioritize compatibility over using the
  latest available version. Choose older, stable API versions when they provide the
  same schema but broader compatibility across Kubernetes versions. This approach
  minimizes breaking changes for users and reduces deployment friction.
repository: istio/istio
label: API
language: Yaml
comments_count: 4
repository_stars: 37192
---

When selecting API versions, prioritize compatibility over using the latest available version. Choose older, stable API versions when they provide the same schema but broader compatibility across Kubernetes versions. This approach minimizes breaking changes for users and reduces deployment friction.

Consider deprecation timelines when making version choices - select versions that give users adequate migration time. For example, prefer `autoscaling/v2beta2` over `autoscaling/v2beta1` when both work, since v2beta2 will be supported longer.

Use conditional logic in templates to handle version selection based on Kubernetes capabilities:

```yaml
{{- if (semverCompare ">=1.23-0" .Capabilities.KubeVersion.GitVersion)}}
apiVersion: autoscaling/v2
{{- else }}
apiVersion: autoscaling/v2beta2
{{- end }}
```

The principle is: "use the oldest version everywhere (it's strictly better - same schema but more compatible, and requires no noise from changing a bunch of files)". Be conservative with API version updates, especially in configurations that directly impact users.