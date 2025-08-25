---
title: Include contextual log information
description: Log messages should include sufficient context to make them useful for
  debugging, monitoring, and audit trails. Include relevant entity IDs, operation
  details, and descriptive information that helps identify what was happening when
  the log entry was created.
repository: discourse/discourse
label: Logging
language: Ruby
comments_count: 4
repository_stars: 44898
---

Log messages should include sufficient context to make them useful for debugging, monitoring, and audit trails. Include relevant entity IDs, operation details, and descriptive information that helps identify what was happening when the log entry was created.

Key practices:
- Include entity IDs (user ID, upload ID, job ID) in log messages
- Add operation context to describe what process was running
- Make error messages descriptive rather than generic
- Log important state changes for audit purposes
- Avoid silent failures - log warnings when operations can't complete normally

Example of good contextual logging:
```ruby
# Good - includes IDs and operation context
Rails.logger.info("Completed video conversion for upload ID #{upload.id} and job ID #{args[:job_id]}")
Rails.logger.error("Upload #{upload.id} URL remained blank after #{MAX_RETRIES} retries when optimizing video")

# Poor - lacks context
Rails.logger.info("Conversion completed")
Rails.logger.error("URL blank after retries")
```

This approach ensures log entries provide actionable information for troubleshooting and create comprehensive audit trails for critical operations like user impersonation or data processing workflows.