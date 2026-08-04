---
title: Triage-Ready Telemetry
description: When implementing observability detections/parsers, ensure alerts/fields
  are (1) schema-correct and vendor-correct, and (2) triage-ready with the exact raw
  context that triggered the signal.
repository: Azure/Azure-Sentinel
label: Observability
language: Yaml
comments_count: 2
repository_stars: 6042
---

When implementing observability detections/parsers, ensure alerts/fields are (1) schema-correct and vendor-correct, and (2) triage-ready with the exact raw context that triggered the signal.

Apply these rules:
1) Validate against the target platform’s allowed schema/values
- If a field has an explicit allowed set (e.g., eventseverity), map upstream values into only those supported values.
- Example guidance (severity mapping):
  - Confirm allowed target values (e.g., Informational/Low/Medium/High).
  - Consult the vendor’s priority/severity documentation.
  - Map each vendor level to a supported target value, and document the rationale (e.g., “CEF Critical→High”).

2) Make anomaly-based alerts actionable
- If you compute anomalies/scores, the alert output should include or join the raw events (or raw aggregates at the anomaly time window) so analysts can immediately see what triggered the anomaly.

KQL pattern (join-back for triage context):
```kql
// 1) Build anomaly signal (score) per user/type
let BinTime = 1h;
let RunTime = 1h;
let LearningPeriod = 7d;
let EndLearningTime = ago(LearningPeriod);
let EndRunTime = ago(RunTime);
let sensitivity = 2.5;

let signal =
    tableName
    | where TimeGenerated between (EndLearningTime .. ago(0))
    | where AppDisplayName =~ "GitHub.com" and ResultType != 0
    | make-series FailedLogins=count() on TimeGenerated from EndLearningTime to EndRunTime step BinTime
      by UserPrincipalName, Type
    | extend (Anomalies, Score, Baseline) = series_decompose_anomalies(FailedLogins, sensitivity, -1, 'linefit')
    | mv-expand TimeGenerated to typeof(datetime), Anomalies to typeof(double)
    | where TimeGenerated >= EndRunTime and Anomalies > 0;

// 2) Join back to raw events at the anomaly time for triage context
signal
| join kind=innerunique (
    tableName
    | where AppDisplayName =~ "GitHub.com" and ResultType != 0
    | summarize RawEventCount=count() by UserPrincipalName, Type, bin(TimeGenerated, BinTime)
) on UserPrincipalName, Type, $left.TimeGenerated == $right.TimeGenerated
```

Practical checklist for PRs
- [ ] Are all normalized fields mapped only to the platform’s supported values?
- [ ] Is upstream/vender semantics verified with a cited source?
- [ ] Does the detection output include raw triggering context at the anomaly time (not only anomaly score)?
- [ ] Is the mapping rationale documented so future changes don’t regress triage quality?