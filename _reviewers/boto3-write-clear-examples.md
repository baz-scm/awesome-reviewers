---
title: Write clear examples
description: 'Create comprehensive code examples in documentation that demonstrate
  common operations and use proper formatting. Use double backticks (``) for inline
  code references in reStructuredText, and wrap code blocks in proper directives:'
repository: boto/boto3
label: Documentation
language: Other
comments_count: 5
repository_stars: 9417
---

Create comprehensive code examples in documentation that demonstrate common operations and use proper formatting. Use double backticks (``) for inline code references in reStructuredText, and wrap code blocks in proper directives:

```
.. code-block:: python

    import boto3
    
    # Create an S3 client
    s3 = boto3.client('s3')
    
    # Upload a file to S3 - this demonstrates the simple method for small files
    s3.upload_file('local/path/to/file', 'my-bucket', 'key/name.txt')
```

Always include explanatory comments that describe what each section accomplishes. For service-specific guides, include examples of frequently used operations like upload/download for S3. When documenting parameters or return values, use accurate descriptions that match the underlying implementation. Always generate and preview documentation before submission to ensure correct rendering.