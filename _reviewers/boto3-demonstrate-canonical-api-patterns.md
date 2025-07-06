---
title: Demonstrate canonical API patterns
description: 'Always provide examples that demonstrate the recommended and most current
  API usage patterns. This includes:


  1. Using the most up-to-date API operations (e.g., prefer ListObjectsV2 over ListObjects)'
repository: boto/boto3
label: API
language: Other
comments_count: 3
repository_stars: 9417
---

Always provide examples that demonstrate the recommended and most current API usage patterns. This includes:

1. Using the most up-to-date API operations (e.g., prefer ListObjectsV2 over ListObjects)
2. Showing proper parameter passing conventions (positional vs. keyword arguments)
3. Including handling for special cases like region-specific logic
4. Testing all examples to verify they work as documented

Examples should be concise but complete enough to show proper usage:

```python
# CORRECT: Proper parameter passing for upload_file (positional arguments)
s3.upload_file(filename, bucket_name, key_name)

# INCORRECT: Attempting to use keyword arguments for positional parameters
s3.upload_file(Bucket=bucket_name, Filename=filename)  # This will fail!

# CORRECT: Handling region-specific bucket creation
bucket_config = {}
if region != "us-east-1":
    bucket_config["CreateBucketConfiguration"] = {"LocationConstraint": region}
s3.create_bucket(Bucket=bucket_name, **bucket_config)

# CORRECT: Using the recommended V2 API version
event_system.register('before-parameter-build.s3.ListObjectsV2', add_my_bucket)
```

Validating examples against the actual implementation helps catch discrepancies between documentation and behavior, ensuring developers can trust your API examples as authoritative references.