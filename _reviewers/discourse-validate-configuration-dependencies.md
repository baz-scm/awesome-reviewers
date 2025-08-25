---
title: Validate configuration dependencies
description: Configuration settings often depend on other settings or external resources
  to function correctly. Always implement validation to check these dependencies and
  provide clear error messages when requirements are not met.
repository: discourse/discourse
label: Configurations
language: Yaml
comments_count: 3
repository_stars: 44898
---

Configuration settings often depend on other settings or external resources to function correctly. Always implement validation to check these dependencies and provide clear error messages when requirements are not met.

When adding new configuration settings:
1. Identify all dependencies (other settings, external services, required credentials)
2. Implement validation that checks these dependencies are satisfied
3. Document interactions with other settings clearly
4. Use appropriate setting types (enums instead of free-form strings when possible)

Example validation pattern:
```yaml
video_conversion_enabled:
  default: false
video_conversion_service:
  enum: "VideoConversionServiceSetting"
  default: "aws_mediaconvert"
```

With corresponding validation: "If `video_conversion_enabled` is true and `video_conversion_service` is `aws_mediaconvert`, then `mediaconvert_role_arn` and S3 credentials must be present."

This prevents runtime failures and reduces user confusion by catching configuration errors early and providing actionable feedback.