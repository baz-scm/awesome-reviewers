---
title: Standardize metrics collection
description: "Use the appropriate metric types for the data being collected and consider\
  \ centralizing monitoring code to ensure consistency across components. \n\nFor\
  \ accumulating values like request counts, use counters rather than gauges:"
repository: kubeflow/kubeflow
label: Observability
language: Go
comments_count: 2
repository_stars: 15064
---

Use the appropriate metric types for the data being collected and consider centralizing monitoring code to ensure consistency across components. 

For accumulating values like request counts, use counters rather than gauges:

```go
// CORRECT: Request counts should use counter metrics
requestCounter = prometheus.NewCounterVec(
    prometheus.CounterOpts{
        Name: "request_counter",
        Help: "Number of request_counter",
    },
    []string{COMPONENT, KIND, NAMESPACE, ACTION, SEVERITY},
)

// INCORRECT: Don't use gauges for request counts
// requestGauge = prometheus.NewGaugeVec(...)
```

To promote consistency, consider extracting common monitoring patterns into a shared library when multiple components need similar metrics. This ensures standardized naming conventions, label sets, and metric types across your application. Standard label keys (like component, namespace, severity) should be defined once and shared to prevent duplication and inconsistency.


[
  {
    "discussion_id": "335548210",
    "pr_number": 4251,
    "pr_file": "components/kf-monitoring/MetricsExporter.go",
    "created_at": "2019-10-16T15:28:17+00:00",
    "commented_code": "package monitoring_util\n\nimport (\n\t\"fmt\"\n\t\"time\"\n\n\t\"github.com/prometheus/client_golang/prometheus\"\n\t\"github.com/prometheus/client_golang/prometheus/promhttp\"\n\t\"github.com/prometheus/common/log\"\n\t\"net\"\n\t\"net/http\"\n)\n\n// Common label keys for all metrics signals\n// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n// COMPONENT: name of Component outputing the metrics, eg. \"tf-operator\"\nconst COMPONENT = \"Component\"\n// KIND: each componenet can label their metrics with custom tag \"kind\". Suggest keeping \"kind\" value to be CONSTANT PER METRICS.\nconst KIND = \"kind\"\nconst NAMESPACE = \"namespace\"\n// ACTION: request action type of the metrics, eg. \"CRUD\"\nconst ACTION = \"action\"\n// SEVERITY: level of importance, used to filter alerts\nconst SEVERITY  = \"severity\"\n// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n\n// Alerting metrics severity levels\n// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\nconst SEVERITY_MINOR = \"Minor\"\nconst SEVERITY_MAJOR = \"Major\"\nconst SEVERITY_CRITICAL = \"Critical\"\n// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n\n// Util const values\n// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\nconst METRICSPORT = 8079\nconst METRICSPATH = \"/metrics\"\n// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n\nvar (\n\t// Counter metrics\n\t// num of requests counter vec\n\trequestCounter = prometheus.NewCounterVec(\n\t\tprometheus.CounterOpts{\n\t\t\tName: \"request_counter\",\n\t\t\tHelp: \"Number of request_counter\",\n\t\t},\n\t\t[]string{COMPONENT, KIND, NAMESPACE, ACTION, SEVERITY},\n\t)\n\t// Counter metrics for failed requests\n\trequestFailureCounter = prometheus.NewCounterVec(prometheus.CounterOpts{\n\t\tName: \"request_failure_counter\",\n\t\tHelp: \"Number of request_failure_counter\",\n\t}, []string{COMPONENT, KIND, NAMESPACE, ACTION, SEVERITY})\n\n\t// Gauge metrics\n\trequestGauge = prometheus.NewGaugeVec(prometheus.GaugeOpts{\n\t\tName: \"requests_gauge\",",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "335548210",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 4251,
        "pr_file": "components/kf-monitoring/MetricsExporter.go",
        "discussion_id": "335548210",
        "commented_code": "@@ -0,0 +1,161 @@\n+package monitoring_util\n+\n+import (\n+\t\"fmt\"\n+\t\"time\"\n+\n+\t\"github.com/prometheus/client_golang/prometheus\"\n+\t\"github.com/prometheus/client_golang/prometheus/promhttp\"\n+\t\"github.com/prometheus/common/log\"\n+\t\"net\"\n+\t\"net/http\"\n+)\n+\n+// Common label keys for all metrics signals\n+// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n+// COMPONENT: name of Component outputing the metrics, eg. \"tf-operator\"\n+const COMPONENT = \"Component\"\n+// KIND: each componenet can label their metrics with custom tag \"kind\". Suggest keeping \"kind\" value to be CONSTANT PER METRICS.\n+const KIND = \"kind\"\n+const NAMESPACE = \"namespace\"\n+// ACTION: request action type of the metrics, eg. \"CRUD\"\n+const ACTION = \"action\"\n+// SEVERITY: level of importance, used to filter alerts\n+const SEVERITY  = \"severity\"\n+// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n+\n+// Alerting metrics severity levels\n+// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n+const SEVERITY_MINOR = \"Minor\"\n+const SEVERITY_MAJOR = \"Major\"\n+const SEVERITY_CRITICAL = \"Critical\"\n+// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n+\n+// Util const values\n+// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n+const METRICSPORT = 8079\n+const METRICSPATH = \"/metrics\"\n+// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n+\n+var (\n+\t// Counter metrics\n+\t// num of requests counter vec\n+\trequestCounter = prometheus.NewCounterVec(\n+\t\tprometheus.CounterOpts{\n+\t\t\tName: \"request_counter\",\n+\t\t\tHelp: \"Number of request_counter\",\n+\t\t},\n+\t\t[]string{COMPONENT, KIND, NAMESPACE, ACTION, SEVERITY},\n+\t)\n+\t// Counter metrics for failed requests\n+\trequestFailureCounter = prometheus.NewCounterVec(prometheus.CounterOpts{\n+\t\tName: \"request_failure_counter\",\n+\t\tHelp: \"Number of request_failure_counter\",\n+\t}, []string{COMPONENT, KIND, NAMESPACE, ACTION, SEVERITY})\n+\n+\t// Gauge metrics\n+\trequestGauge = prometheus.NewGaugeVec(prometheus.GaugeOpts{\n+\t\tName: \"requests_gauge\",",
        "comment_created_at": "2019-10-16T15:28:17+00:00",
        "comment_author": "yeya24",
        "comment_body": "Requests should not be a gauge value. From my thought, requests are only appropriate for counter.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "369267781",
    "pr_number": 4674,
    "pr_file": "components/access-management/kfam/monitoring.go",
    "created_at": "2020-01-21T22:04:06+00:00",
    "commented_code": "package kfam",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "369267781",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 4674,
        "pr_file": "components/access-management/kfam/monitoring.go",
        "discussion_id": "369267781",
        "commented_code": "@@ -0,0 +1,67 @@\n+package kfam",
        "comment_created_at": "2020-01-21T22:04:06+00:00",
        "comment_author": "zhenghuiwang",
        "comment_body": "Do we expect other KF components to follow this pattern(same set of counter names, types etc)? If so, can it be put as a library outside `kfam`? ",
        "pr_file_module": null
      },
      {
        "comment_id": "369271243",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 4674,
        "pr_file": "components/access-management/kfam/monitoring.go",
        "discussion_id": "369267781",
        "commented_code": "@@ -0,0 +1,67 @@\n+package kfam",
        "comment_created_at": "2020-01-21T22:12:36+00:00",
        "comment_author": "kunmingg",
        "comment_body": "We can put that effort into v1.0.1 and avoid blocking release of v1.0.0?\r\n@jlewi \r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "369341746",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 4674,
        "pr_file": "components/access-management/kfam/monitoring.go",
        "discussion_id": "369267781",
        "commented_code": "@@ -0,0 +1,67 @@\n+package kfam",
        "comment_created_at": "2020-01-22T02:19:15+00:00",
        "comment_author": "jlewi",
        "comment_body": "+1 I suspect we will likely need to do some more refactoring post 1.0 as we will identify missing metrics etc... so I would be in favor of getting this merged now and then taking a more holistic look at our monitoring.",
        "pr_file_module": null
      }
    ]
  }
]
