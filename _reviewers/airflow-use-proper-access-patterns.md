---
title: Use proper access patterns
description: 'Access configurations through documented abstraction layers rather than
  bypassing them with direct database or low-level access. For example, in Airflow,
  XCom operations should be performed through the Task Context using `get_current_context()`
  rather than directly accessing the database model:'
repository: apache/airflow
label: Configurations
language: Other
comments_count: 2
repository_stars: 40858
---

Access configurations through documented abstraction layers rather than bypassing them with direct database or low-level access. For example, in Airflow, XCom operations should be performed through the Task Context using `get_current_context()` rather than directly accessing the database model:

```python
# Good practice
from airflow.sdk import get_current_context

def my_task(**context):
    # Alternatively: context = get_current_context()
    # Pull XCom value
    value = context["ti"].xcom_pull(task_ids="previous_task")
    # Push XCom value
    context["ti"].xcom_push(key="my_key", value="my_value")
```

For version-dependent configurations, use explicit version comparison functions (like `semverCompare` in Helm) rather than hard-coding version assumptions:

{% raw %}
```yaml
# Good practice (Helm example)
{{- if and (semverCompare "<3.0.0" .Values.airflowVersion) (or .Values.webserver.webserverConfig .Values.webserver.webserverConfigConfigMapName) }}
# Version-specific configuration here
{{- end }}
```
{% endraw %}