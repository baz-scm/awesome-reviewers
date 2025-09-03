---
title: Environment variable documentation
description: Ensure comprehensive and accurate documentation of environment variables,
  including cross-references, auto-detection behavior, and deployment context. When
  documenting configuration options, always provide links to the environment variables
  page and specify the exact variable name. Include information about auto-detected
  variables that Langflow recognizes...
repository: langflow-ai/langflow
label: Configurations
language: Other
comments_count: 6
repository_stars: 111046
---

Ensure comprehensive and accurate documentation of environment variables, including cross-references, auto-detection behavior, and deployment context. When documenting configuration options, always provide links to the environment variables page and specify the exact variable name. Include information about auto-detected variables that Langflow recognizes by default, and provide deployment-specific context such as Docker usage.

For example, when documenting file upload configuration:
```markdown
Increased the default maximum size for file uploads from 100 MB to 1024 MB.
You can configure this with the [`LANGFLOW_MAX_FILE_SIZE_UPLOAD`](/environment-variables#LANGFLOW_MAX_FILE_SIZE_UPLOAD) environment variable.

When running a Langflow Docker image, the `-e` flag sets system environment variables:
```bash
docker run -e LANGFLOW_MAX_FILE_SIZE_UPLOAD=2048 langflow
```

Additionally, document the precise behavior and interactions between related environment variables. For complex variables like authentication settings, clearly explain conditional behavior:
```markdown
If set to `true`, and `LANGFLOW_AUTO_LOGIN` is set to `true`, skips authentication and allows automatic login as the superuser. If `LANGFLOW_AUTO_LOGIN` is `false`, has no effect.
```

This ensures users understand not just what variables exist, but how to use them effectively across different deployment scenarios and how they interact with other configuration options.