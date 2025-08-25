---
title: Include contextual error information
description: Error messages should include relevant contextual information such as
  IDs, file paths, job identifiers, and other debugging details to make troubleshooting
  easier. Generic error messages make it difficult to identify the specific instance
  or operation that failed, especially in systems processing multiple items concurrently.
repository: discourse/discourse
label: Error Handling
language: Ruby
comments_count: 3
repository_stars: 44898
---

Error messages should include relevant contextual information such as IDs, file paths, job identifiers, and other debugging details to make troubleshooting easier. Generic error messages make it difficult to identify the specific instance or operation that failed, especially in systems processing multiple items concurrently.

When logging errors, include:
- Entity IDs (upload_id, user_id, job_id, etc.)
- File paths or URLs being processed
- Operation context or step information
- Request IDs when available

Example of improved error logging:

```ruby
# Poor: Generic error message
Rails.logger.error("Failed to handle video conversion completion")

# Good: Contextual error message  
Rails.logger.error("Failed to handle video conversion completion for upload ID #{upload.id} and job ID #{args[:job_id]}")

# Poor: Missing context in model errors
Rails.logger.error("Failed to create optimized video: #{optimized_video.errors.full_messages.join(", ")}")

# Good: Include relevant entity context
Rails.logger.error("Failed to create optimized video for upload ID #{upload.id}: #{optimized_video.errors.full_messages.join(", ")}")
```

This practice significantly reduces debugging time and helps identify patterns in failures across different environments and deployments.