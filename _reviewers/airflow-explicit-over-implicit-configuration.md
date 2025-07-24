---
title: Explicit over implicit configuration
description: Always prefer explicit configuration parameters over inferring behavior
  from indirect sources like image tags, naming conventions, or environment factors.
  When behavior needs to vary based on environment or version, introduce dedicated
  configuration parameters that users can explicitly set rather than relying on potentially
  unreliable metadata.
repository: apache/airflow
label: Configurations
language: Yaml
comments_count: 4
repository_stars: 40858
---

Always prefer explicit configuration parameters over inferring behavior from indirect sources like image tags, naming conventions, or environment factors. When behavior needs to vary based on environment or version, introduce dedicated configuration parameters that users can explicitly set rather than relying on potentially unreliable metadata.

This practice ensures that:
1. Configuration remains predictable even when users customize their environment
2. Breaking changes are avoided when indirect factors change
3. System behavior is easier to debug and understand

For example, instead of:
{% raw %}
```yaml
# DON'T: Inferring behavior from image tag
{{- if hasPrefix .Values.images.gitSync.tag "v3" }}
  # Use v3 configuration
{{- else }}
  # Use v4 configuration
{{- end }}
```
{% endraw %}

Use:
{% raw %}
```yaml
# DO: Explicit configuration parameter
gitSync:
  version: "v4"  # Explicit parameter users can set
{{- if eq .Values.gitSync.version "v3" }}
  # Use v3 configuration
{{- else }}
  # Use v4 configuration
{{- end }}
```
{% endraw %}

When adding configuration parameters that might interact with existing ones, clearly document their relationships and ensure proper handling of all cases. For instance, document when certain parameters might be ignored under specific conditions, and consider providing mechanisms to merge or append user-defined values with defaults.