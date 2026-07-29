---
title: Explicit Null Safety
description: 'When templating, explicitly distinguish three states: **missing**, **explicit
  false**, and **null**. Relying on truthiness can silently drop intended configuration.'
repository: maximhq/bifrost
label: Null Handling
language: Yaml
comments_count: 2
repository_stars: 6862
---

When templating, explicitly distinguish three states: **missing**, **explicit false**, and **null**. Relying on truthiness can silently drop intended configuration.

**Apply two patterns:**
1) **Preserve explicit `false`** (boolean fields)
- Don’t use `with` / truthy checks for booleans if `false` must still render.
- Instead, render based on **key presence**.

```gotemplate
{{/* BAD: with treats false as empty */}}
{{- with .Values.serviceMonitor.honorLabels }}
honorLabels: {{ . }}
{{- end }}

{{/* GOOD: preserves explicit false */}}
{{- if hasKey .Values.serviceMonitor "honorLabels" }}
honorLabels: {{ .Values.serviceMonitor.honorLabels }}
{{- end }}
```

2) **Omit fields via real null (Helm values)**
- If you need to remove defaulted keys so downstream controllers (e.g., SCCs) can assign values, override with **`null`** (and confirm rendered output).
- Use `helm template` to verify that `runAsUser: null` / `fsGroup: null` (or similar) do **not** appear in manifests.

```yaml
# values.yaml override example
podSecurityContext:
  runAsUser: null
  fsGroup: null
securityContext:
  runAsUser: null
```

**Rule of thumb:**
- If `false` must be honored → **check `hasKey`**.
- If a value must be removed from rendered YAML → **override with `null`** and verify with `helm template`.