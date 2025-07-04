---
title: Configure proxies with schemes
description: 'When configuring proxies in AWS SDK clients, always include the complete
  URL scheme in proxy definitions. Match the scheme to the protocol: use ''http://''
  for HTTP connections and ''https://'' for HTTPS connections. Missing or incorrect
  schemes can lead to connection failures or security issues.'
repository: boto/boto3
label: Networking
language: Other
comments_count: 5
repository_stars: 9417
---

When configuring proxies in AWS SDK clients, always include the complete URL scheme in proxy definitions. Match the scheme to the protocol: use 'http://' for HTTP connections and 'https://' for HTTPS connections. Missing or incorrect schemes can lead to connection failures or security issues.

For example, when setting up proxies with the Config object:

```python
import boto3
from botocore.config import Config

# Correct way to define proxies with proper schemes
proxy_definitions = {
    'http': 'http://proxy.company.com:6502',  # HTTP scheme for HTTP proxy
    'https': 'https://proxy.company.com:2010'  # HTTPS scheme for HTTPS proxy
}

my_config = Config(
    region_name='us-east-2',
    proxies=proxy_definitions
)

client = boto3.client('s3', config=my_config)
```

Remember that TLS negotiation only occurs with HTTPS connections, so when configuring proxy_ca_bundle or proxy_client_cert in proxies_config, ensure you're using HTTPS proxies. Otherwise, your certificate configuration will have no effect.