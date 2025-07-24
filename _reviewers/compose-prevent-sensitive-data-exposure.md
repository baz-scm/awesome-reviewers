---
title: Prevent sensitive data exposure
description: Implement comprehensive checks to prevent accidental exposure of sensitive
  data through multiple vectors in configuration files and deployment artifacts. This
  includes validating environment variables, file permissions, bind mounts, and individual
  configuration files before publishing or deployment.
repository: docker/compose
label: Security
language: Go
comments_count: 4
repository_stars: 35858
---

Implement comprehensive checks to prevent accidental exposure of sensitive data through multiple vectors in configuration files and deployment artifacts. This includes validating environment variables, file permissions, bind mounts, and individual configuration files before publishing or deployment.

Key practices:
1. **Environment variables**: Block publication of compose files containing environment variables or env_files by default, requiring explicit opt-in flags to prevent accidental secret leaks
2. **Individual file validation**: Check each individual file in compose projects for sensitive data, not just the final merged model, as secrets may be present in individual files even if overridden
3. **File permissions**: Use restrictive permissions for sensitive files (e.g., 0o440 for secrets vs 0o444 for regular configs) to limit access
4. **User warnings**: Provide clear warnings when potentially sensitive data like bind mount declarations will be included in artifacts

Example implementation:
```go
func preChecks(project *types.Project, options api.PublishOptions) error {
    if !options.WithEnvironment {
        for _, service := range project.Services {
            if len(service.Environment) > 0 {
                return fmt.Errorf("service %q has environment variable(s) declared. To avoid leaking sensitive data, " +
                    "you must either explicitly allow the sending of environment variables by using the --with-env flag")
            }
        }
    }
    // Check individual files, not just final model
    // Validate bind mounts with user warnings
    // Apply restrictive permissions for secrets
}
```

This approach ensures multiple layers of protection against sensitive data exposure while maintaining usability through explicit opt-in mechanisms.