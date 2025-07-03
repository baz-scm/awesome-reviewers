---
title: Test configuration precedence
description: When implementing systems that load configuration from multiple sources,
  always test the precedence rules explicitly to ensure the correct values are being
  used. Configuration loading bugs can be subtle and difficult to diagnose in production.
repository: aws/aws-sdk-js
label: Configurations
language: Other
comments_count: 3
repository_stars: 7628
---

When implementing systems that load configuration from multiple sources, always test the precedence rules explicitly to ensure the correct values are being used. Configuration loading bugs can be subtle and difficult to diagnose in production.

For example, when testing credential loading from multiple files or environment variables:

```javascript
it('loads credentials from preferred source when available in multiple locations', () => {
  // Set up multiple configuration sources
  process.env.AWS_SDK_LOAD_CONFIG = '1';
  helpers.spyOn(AWS.util, 'readFileSync').andCallFake((path) => {
    if (path.match(/credentials/)) {
      return '...[credentials file content]...';
    } else {
      return '...[config file content]...';
    }
  });
  
  // Create a spy to verify which credentials are actually used
  const credentialSpy = helpers.spyOn(AWS.STS.prototype, 'makeRequest')
    .andCallThrough();
  
  // Exercise the code that loads credentials
  const creds = new AWS.SharedIniFileCredentials();
  creds.get();
  
  // Verify the correct source was used
  expect(credentialSpy.calls[0].arguments[1].accessKeyId)
    .to.equal('expected-key-from-preferred-source');
});
```

Don't just verify that configuration loads successfully—explicitly test that the correct values from the highest-priority source are being used when the same configuration option exists in multiple places.
