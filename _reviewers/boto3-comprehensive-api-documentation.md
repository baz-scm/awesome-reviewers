---
title: Comprehensive API documentation
description: Always provide comprehensive API documentation that includes accurate
  examples, complete parameter descriptions, and clarifications about parameter usage.
  This helps users understand how to properly use your API and reduces support questions.
repository: boto/boto3
label: Documentation
language: Python
comments_count: 6
repository_stars: 9417
---

Always provide comprehensive API documentation that includes accurate examples, complete parameter descriptions, and clarifications about parameter usage. This helps users understand how to properly use your API and reduces support questions.

1. **Include multiple usage examples** showing different common scenarios:

```python
# Example showing file path operations with proper mode
with open('/tmp/myfile.txt', 'rb') as file:
    s3.upload_fileobj(file, 'mybucket', 'mykey')

# Example showing in-memory operations
import io
data = io.BytesIO(b'file content')
s3.upload_fileobj(data, 'mybucket', 'mykey')
```

2. **Document all parameters** with:
   - Type information
   - Clear description of purpose
   - Default values or required status
   - Which operation the parameter applies to (for complex methods)

```python
def upload_fileobj(self, Fileobj, Bucket, Key, ExtraArgs=None, Callback=None, Config=None):
    """Upload a file-like object to S3.
    
    :type Fileobj: file-like object
    :param Fileobj: A file-like object that implements read()
    
    :type Bucket: str
    :param Bucket: The name of the bucket to upload to
    
    :type ExtraArgs: dict
    :param ExtraArgs: Extra arguments that will be passed to the underlying
                     PutObject operation (e.g., {'ACL': 'public-read'})
    """
```

3. **Use correct documentation syntax** for your chosen documentation system:
   - In restructuredText, use double backticks (``code``) for inline code
   - Use relative links instead of absolute URLs
   - Ensure API examples use accurate methods (e.g., distinguish between `boto3.client('s3')` and `boto3.resource('s3')`)

Always test your documentation examples to verify they work as described.