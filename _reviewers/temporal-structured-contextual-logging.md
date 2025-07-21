---
title: Structured contextual logging
description: Always use structured logging with appropriate tags instead of string
  concatenation or formatting. Include relevant contextual information that would
  help in troubleshooting, such as namespace, operation ID, or workflow ID.
repository: temporalio/temporal
label: Logging
language: Go
comments_count: 3
repository_stars: 14953
---

Always use structured logging with appropriate tags instead of string concatenation or formatting. Include relevant contextual information that would help in troubleshooting, such as namespace, operation ID, or workflow ID.

**Instead of this:**
```go
logger.Debug("ShowTaskQueueConfig : " + strconv.FormatBool(req.ShowTaskQueueConfig))
logger.Info(fmt.Sprintf("Removed expired workflow rule %s", oldestKey))
```

**Do this:**
```go
logger.Debug("Show task queue config", tag.Bool("showTaskQueueConfig", req.ShowTaskQueueConfig))
logger.Info("Removed expired workflow rule", tag.WorkflowRuleID(oldestKey), tag.WorkflowNamespaceID(namespaceID))
```

Structured logging with proper context tags makes logs:
- More consistent and standardized across the codebase
- Easier to search, filter, and aggregate
- Machine-parsable for log analysis tools
- More useful when diagnosing issues

Always consider what contextual information would be helpful for someone debugging an issue, and include those as tags rather than embedding them in the message text.