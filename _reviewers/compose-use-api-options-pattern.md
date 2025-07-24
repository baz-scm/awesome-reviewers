---
title: Use API options pattern
description: Design API methods using options objects instead of multiple parameters.
  This pattern provides better extensibility, version compatibility, and maintains
  consistent interfaces across the codebase.
repository: docker/compose
label: API
language: Go
comments_count: 4
repository_stars: 35858
---

Design API methods using options objects instead of multiple parameters. This pattern provides better extensibility, version compatibility, and maintains consistent interfaces across the codebase.

Benefits:
- Prevents frequent API refactoring when new parameters are needed
- Enables graceful version-specific feature handling
- Maintains backward compatibility
- Simplifies parameter documentation

Example:
```go
// Instead of this:
func (s *Service) Publish(ctx context.Context, project *types.Project, repository string) error {
    // ...
}

// Do this:
type PublishOptions struct {
    Project     *types.Project
    Repository  string
    Quiet       bool    // Future-proof for additional options
}

func (s *Service) Publish(ctx context.Context, opts PublishOptions) error {
    // Version-specific feature check example
    if opts.NewFeature != nil {
        version, err := s.RuntimeVersion(ctx)
        if err != nil {
            return err
        }
        if versions.LessThan(version, "1.44") {
            return errors.New("feature requires Docker Engine 1.44 or later")
        }
    }
    // ...
}
```