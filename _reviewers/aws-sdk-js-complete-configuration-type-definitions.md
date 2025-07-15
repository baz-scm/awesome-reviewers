---
title: Complete configuration type definitions
description: Ensure configuration type definitions are complete and consistent between
  global and service-specific settings. When designing configuration classes, include
  service identifiers as optional instance variables and ensure update methods accept
  all relevant option types that might be used at both global and service-specific
  levels.
repository: aws/aws-sdk-js
label: Configurations
language: TypeScript
comments_count: 2
repository_stars: 7628
---

Ensure configuration type definitions are complete and consistent between global and service-specific settings. When designing configuration classes, include service identifiers as optional instance variables and ensure update methods accept all relevant option types that might be used at both global and service-specific levels.

Example:
```typescript
// Proper configuration class definition
export class Config {
  // Service identifiers as optional properties
  s3?: ServiceConfigurationOptions;
  dynamodb?: ServiceConfigurationOptions;
  
  // Update method that accepts all relevant option types
  update(options: ConfigurationOptions & 
         ConfigurationServicePlaceholders & 
         APIVersions & 
         CredentialsOptions, 
         allowUnknownKeys?: boolean): void;
}

// Usage example
AWS.config.s3 = {params: {Bucket: 'myBucket'}, useDualstack: true};
```

This approach prevents TypeScript compiler errors when users set valid configurations and maintains consistency between global and service-specific configuration options.
