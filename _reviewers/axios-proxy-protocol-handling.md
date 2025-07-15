---
title: "Proxy protocol handling"
description: "When implementing HTTP clients with proxy support, ensure the connection to the proxy uses the protocol specified in the proxy configuration (not the request protocol). This is crucial for scenarios like accessing HTTPS resources through an HTTP proxy."
repository: "axios/axios"
label: "Networking"
language: "JavaScript"
comments_count: 5
repository_stars: 107000
---

When implementing HTTP clients with proxy support, ensure the connection to the proxy uses the protocol specified in the proxy configuration (not the request protocol). This is crucial for scenarios like accessing HTTPS resources through an HTTP proxy.

Key implementation guidelines:
- Use the proxy's protocol for the connection to the proxy server
- Implement HTTP CONNECT tunneling for HTTPS destinations through proxies
- Parse proxy URLs correctly using the `hostname` property (not `host`)
- Support common proxy environment variables including fallbacks

```javascript
function configureProxy(options, config) {
  // Check for explicitly configured proxy
  let proxy = config.proxy;
  
  if (!proxy) {
    // Check for environment variables
    const proxyEnv = parsed.protocol.slice(0, -1) + '_proxy';
    const proxyUrl = process.env[proxyEnv] || 
                     process.env[proxyEnv.toUpperCase()] ||
                     process.env.all_proxy || 
                     process.env.ALL_PROXY;
    
    if (proxyUrl) {
      const parsedProxyUrl = url.parse(proxyUrl);
      proxy = {
        host: parsedProxyUrl.hostname,  // Use hostname, not host (which includes port)
        port: parsedProxyUrl.port,
        protocol: parsedProxyUrl.protocol
      };
      
      // Handle proxy authentication if present
      if (parsedProxyUrl.auth) {
        // Configure proxy authentication
      }
    }
  }
  
  if (proxy) {
    // Use proxy's protocol for connection to proxy
    // Set up tunneling for HTTPS requests through HTTP proxy
    const usesTunnel = proxy.protocol === "http:" && options.protocol === "https:";
    if (usesTunnel) {
      // Configure HTTP CONNECT tunneling
    }
  }
  
  return options;
}
```