---
title: Arm Escape In Configs
description: When authoring Sentinel solution/connector configuration JSON (especially
  CCF/CCP connector `*_PollerConfig.json` and embedded/packaged `mainTemplate.json`
  content templates), treat `[[ ...` as a configuration-time escape—do not “simplify”
  it.
repository: Azure/Azure-Sentinel
label: Configurations
language: Json
comments_count: 6
repository_stars: 6042
---

When authoring Sentinel solution/connector configuration JSON (especially CCF/CCP connector `*_PollerConfig.json` and embedded/packaged `mainTemplate.json` content templates), treat `[[ ...` as a configuration-time escape—do not “simplify” it.

Rule:
- Use `[[` (double opening bracket) to emit a *literal* ARM expression start `[` into the nested connector template, so the inner template evaluates it later.
- Do **not** convert `[[expr]` to `[expr]` in these nested/preserved contexts; that typically causes the *outer* template to evaluate parameters too early (leading to deployment/runtime failures).
- Do **not** “balance” the escape by changing the closing to `]]`; the correct form is double-open, single-close (and the rest of the expression must remain intact).
- Preserve required quoting where the packaging tool does token substitution (e.g., tokens like `parameters('workspace')` may need to remain quoted as required by the packaging convention).

Example (poller config):
```json
{
  "name": "[[concat('parameters(\"workspace\" )', '/Microsoft.SecurityInsights/SomeTable', uniqueString(parameters('PortfolioId')))]",
  "auth": {
    "type": "APIKey",
    "ApiKey": "[[base64(concat(parameters('apiToken'), ':'))]"
  },
  "request": {
    "apiEndpoint": "[[concat(parameters('endpointUrl'), '/Client/Anomaly')]"
  }
}
```

Checklist before approval:
- Any ARM-like expression inside CCF/CCP connector JSON that must be evaluated at *connector deployment/connect time* should use the documented escaping form.
- Any diff that changes `[[ ...` to `[ ...` (or introduces `]]`) should be treated as a high-risk configuration change requiring explicit justification and validation.