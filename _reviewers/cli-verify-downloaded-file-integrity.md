---
title: verify downloaded file integrity
description: Always verify the integrity of downloaded files before using them, especially
  in security-sensitive applications. At minimum, validate downloaded files using
  checksums (SHA256, etc.) provided by the source. For higher security requirements,
  implement cryptographic signature verification using GPG keys.
repository: snyk/cli
label: Security
language: Python
comments_count: 2
repository_stars: 5178
---

Always verify the integrity of downloaded files before using them, especially in security-sensitive applications. At minimum, validate downloaded files using checksums (SHA256, etc.) provided by the source. For higher security requirements, implement cryptographic signature verification using GPG keys.

Hash verification should occur immediately after download and before caching or extraction:

```python
def download_and_verify(url, expected_hash, filepath):
    # Download file
    urllib.request.urlretrieve(url, filepath)
    
    # Verify hash
    with open(filepath, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    
    if file_hash != expected_hash:
        os.remove(filepath)
        raise ValueError("File integrity check failed")
    
    return filepath
```

For critical applications, extend this with GPG signature verification using trusted public keys. This prevents supply chain attacks and ensures the authenticity of downloaded binaries, libraries, or configuration files.