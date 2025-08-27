---
title: Flexible configuration defaults
description: Configuration values should provide sensible defaults while remaining
  adaptable to different environments and deployment contexts. Use conditional assignment
  and guards to handle variations in runtime environments, deployment tools, and system
  configurations.
repository: istio/istio
label: Configurations
language: Other
comments_count: 2
repository_stars: 37192
---

Configuration values should provide sensible defaults while remaining adaptable to different environments and deployment contexts. Use conditional assignment and guards to handle variations in runtime environments, deployment tools, and system configurations.

For build configurations, use conditional assignment to allow environment-specific overrides:
```makefile
# Allow override for different systems (e.g., NixOS)
SHELL ?= /bin/bash
```

For template configurations, add guards around optional values that may not be available in all contexts:
```yaml
{{- define "istio-labels" }}
    app.kubernetes.io/name: ztunnel
    {{- if .Release.Service }}
    app.kubernetes.io/managed-by: {{ .Release.Service }}
    {{- end }}
{{- end }}
```

This approach ensures configurations work reliably across different deployment methods (helm install, helm template, istioctl) and system environments without requiring manual intervention or causing failures when optional values are missing.