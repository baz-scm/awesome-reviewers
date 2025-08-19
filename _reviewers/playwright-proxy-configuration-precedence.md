---
title: proxy configuration precedence
description: Ensure proxy configuration follows proper precedence hierarchy and handles
  different proxy types correctly. User-specified proxy settings should always take
  priority over environment variables, similar to how browsers handle proxy configuration.
repository: microsoft/playwright
label: Networking
language: TypeScript
comments_count: 6
repository_stars: 76113
---

Ensure proxy configuration follows proper precedence hierarchy and handles different proxy types correctly. User-specified proxy settings should always take priority over environment variables, similar to how browsers handle proxy configuration.

When implementing proxy support:

1. **Prioritize user configuration over environment variables**:
```typescript
getProxyAgent(host: string, port: number) {
  const proxyFromEnv = getProxyForUrl(`https://${host}:${port}`);
  if (proxyFromEnv)
    return createProxyAgent({ server: proxyFromEnv });
  return createProxyAgent(this._proxy); // User config takes precedence
}
```

2. **Map proxy protocols correctly** - use `sslProxy` for HTTPS connections, not `httpsProxy`:
```typescript
switch (url.protocol) {
  case 'http:':
    proxy.httpProxy = url.host;
    break;
  case 'https:':
    proxy.sslProxy = url.host; // Not httpsProxy
    break;
}
```

3. **Handle legacy URL formats gracefully** while planning migration to modern URL objects:
```typescript
// TODO: switch to URL instance instead of legacy object once https-proxy-agent supports it.
return new HttpsProxyAgent(convertURLtoLegacyUrl(proxyOpts));
```

4. **Consider localhost proxy behavior** - some environments require explicit configuration to proxy localhost traffic, which should be handled appropriately for testing scenarios.

This approach ensures consistent proxy behavior across different network scenarios and maintains compatibility with existing proxy infrastructure while preparing for future modernization.