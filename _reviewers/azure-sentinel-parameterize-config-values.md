---
title: Parameterize Config Values
description: When authoring queries/parsers and deployment templates, ensure all environment-
  or customer-specific values are configurable via parameters (e.g., `let`, `ParserParams`,
  CloudFormation `Parameters`), and avoid unsafe sample/environment defaults. Also,
  if you introduce or rely on a standard configuration flag (e.g., additional-fields
  “pack”), make sure it’s...
repository: Azure/Azure-Sentinel
label: Configurations
language: Yaml
comments_count: 6
repository_stars: 6042
---

When authoring queries/parsers and deployment templates, ensure all environment- or customer-specific values are configurable via parameters (e.g., `let`, `ParserParams`, CloudFormation `Parameters`), and avoid unsafe sample/environment defaults. Also, if you introduce or rely on a standard configuration flag (e.g., additional-fields “pack”), make sure it’s supported in both the specific parser and any unifying/wrapper parser so behavior is consistent.

How to apply:
- Replace hardcoded constants with `let` variables and document the default in the query description (e.g., domain allow/target values, thresholds).
- In CloudFormation (or other deployment configs), don’t keep environment-specific bucket/queue name defaults; require explicit inputs when collisions or latent failures are possible.
- Avoid parameters that can silently change behavior by filtering/dropping data without errors; either remove them or implement safe, clearly bounded behavior.
- For parser feature flags/params (e.g., `pack`), wire the parameter through any unifying parser/wrapper.

Example (KQL using `let` for customer override):
```kql
// Configurable targets
let TargetDomain = 'contoso.com';
let SpoofDetectionLookback = 1d;

EmailEvents
| where TimeGenerated > ago(SpoofDetectionLookback)
| where DetectionMethods contains 'spoof'
| where SenderFromDomain has TargetDomain
```

Example (configurable threshold + documented default):
```kql
let TopNMinCount = 5; // default cutoff; increase/decrease as needed
EmailEvents
| where ThreatTypes has 'Malware' or ThreatTypes has 'Phish'
| summarize count() by SenderIPv4
| where count_ > TopNMinCount
```