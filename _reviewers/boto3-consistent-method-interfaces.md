---
title: Consistent method interfaces
description: Design APIs with consistent method interfaces across related resources
  to improve usability and reduce learning curve. When similar operations are available
  on different resources, they should follow the same naming conventions, parameter
  structures, and behavior patterns.
repository: boto/boto3
label: API
language: Python
comments_count: 5
repository_stars: 9417
---

Design APIs with consistent method interfaces across related resources to improve usability and reduce learning curve. When similar operations are available on different resources, they should follow the same naming conventions, parameter structures, and behavior patterns.

Key principles:

1. **Mirror common operations across resources**: When a method makes sense for multiple resource types, provide it consistently. For example, if users can upload files to S3 objects via `client.upload_file()`, they should also be able to do it via `bucket.upload_file()` with consistent parameters.

2. **Handle parameters consistently**: Use the same parameter names and structures for similar operations. If `ExtraArgs` is used in one method to pass additional options, use it consistently in related methods.

```python
# Example of consistent method interfaces across resources
# Client-level method
s3.meta.client.upload_file('filename.txt', 'bucket-name', 'key')

# Same method available at bucket level with identical parameter structure
bucket = s3.Bucket('bucket-name')
bucket.upload_file('filename.txt', 'key')
```

3. **Consider cross-resource operations**: When designing methods that operate across resources (like copying between buckets), carefully consider authentication needs and parameter mapping between underlying API calls.

4. **Provide appropriate configuration options**: Allow users to customize behavior through configuration objects that can be reused across operations and applied consistently.

5. **Document parameter behavior**: Clearly document how parameters map to underlying operations, especially when a high-level method may call multiple lower-level operations with different parameter requirements.

Following these principles results in intuitive APIs where users can confidently apply knowledge from one part of the API to another, reducing friction and improving developer productivity.