---
title: Avoid code duplication
description: Extract repeated code patterns into reusable functions, variables, or
  constants to improve maintainability and reduce the risk of inconsistencies. Look
  for similar code blocks that perform the same operations and consolidate them.
repository: apache/airflow
label: Code Style
language: Python
comments_count: 6
repository_stars: 40858
---

Extract repeated code patterns into reusable functions, variables, or constants to improve maintainability and reduce the risk of inconsistencies. Look for similar code blocks that perform the same operations and consolidate them.

For repeated code blocks:
```python
# Instead of duplicated validation code:
def _validate_inputs(self):
    """Validate required inputs."""
    missing_fields = []
    for field_name in ["sink_name", "project_id"]:
        if not getattr(self, field_name):
            missing_fields.append(field_name)

    if missing_fields:
        raise AirflowException(
            f"Required parameters are missing: {missing_fields}. These parameters must be passed as "
            "keyword parameters or as extra fields in Airflow connection definition."
        )
        
# Prefer a shared validation function:
def validate_required_fields(obj, fields):
    """Validate that required fields are present."""
    missing_fields = []
    for field_name in fields:
        if not getattr(obj, field_name):
            missing_fields.append(field_name)

    if missing_fields:
        raise AirflowException(
            f"Required parameters are missing: {missing_fields}. These parameters must be passed as "
            "keyword parameters or as extra fields in Airflow connection definition."
        )
```

For repeated values:
```python
# Instead of:
command = ["sudo", "-E", "-H", "-u", run_as_user, sys.executable, "-c", rexec_python_code]
log.info("Running command", command=command)
os.execvp("sudo", command)

# Store in a variable to avoid duplication:
command = ["sudo", "-E", "-H", "-u", run_as_user, sys.executable, "-c", rexec_python_code]
log.info("Running command", command=command)
os.execvp("sudo", command)
```

For repeated logic:
```python
# Instead of repeated conditionals:
if len(order_by_list) >= 1:
    order_by_columns.append(self.get_column_with_sort(order_by_list[0]))
if len(order_by_list) == 2:
    order_by_columns.append(self.get_column_with_sort(order_by_list[1]))

# Use a loop:
for i in range(min(len(order_by_list), MAX_SORT_PARAMS)):
    order_by_columns.append(self.get_column_with_sort(order_by_list[i]))
```