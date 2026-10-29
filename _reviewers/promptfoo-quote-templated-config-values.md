---
title: Quote templated config values
description: When Helm chart values (or other YAML-driven config) are interpolated
  into templates as string fields—such as `ingressClassName`, `storageClassName`,
  or similar identifiers—always wrap them in explicit quotes in the template. YAML
  parsers coerce unquoted bare words that look numeric (e.g. a class named `123`)
  into numbers, which breaks the manifest at apply...
repository: promptfoo/promptfoo
label: Configurations
language: Yaml
comments_count: 4
repository_stars: 26565
---

When Helm chart values (or other YAML-driven config) are interpolated into templates as string fields—such as `ingressClassName`, `storageClassName`, or similar identifiers—always wrap them in explicit quotes in the template. YAML parsers coerce unquoted bare words that look numeric (e.g. a class named `123`) into numbers, which breaks the manifest at apply time even though the chart renders without error. For example:

```yaml
{{- with .Values.ingress.className }}
ingressClassName: {{ . | quote }}
{{- end }}
```

and similarly for `storageClassName` whether it comes from values or is inferred from an existing resource. Add a render test that uses a numeric-looking value (like `123`) for any such field so the suite fails if quoting is ever dropped.

Beyond quoting, keep configuration defaults minimal and non-surprising: avoid baking in restrictive defaults (e.g., an `amd64`-only `nodeSelector`) that users on other platforms would have to override, but do set safe, working defaults for security-sensitive fields (e.g., `runAsUser`, `fsGroup`) when the image has known requirements, and document how map-type values merge with user overrides. Treat fields that cannot be changed after creation (like an existing PVC's `storageClassName`) as sticky—preserve the explicitly-set value across upgrades rather than letting a cluster default silently take over.