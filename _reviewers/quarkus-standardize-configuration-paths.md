---
title: Standardize configuration paths
description: Follow consistent patterns for storing and referencing configuration
  files across projects. Place custom configuration files in standardized locations
  (e.g., `src/main/docker` for Dockerfiles, `.s2i` for S2I environment files) and
  use consistent naming conventions. When referencing file paths in configuration
  properties, use relative paths from the project...
repository: quarkusio/quarkus
label: Configurations
language: Other
comments_count: 10
repository_stars: 14667
---

Follow consistent patterns for storing and referencing configuration files across projects. Place custom configuration files in standardized locations (e.g., `src/main/docker` for Dockerfiles, `.s2i` for S2I environment files) and use consistent naming conventions. When referencing file paths in configuration properties, use relative paths from the project root to ensure portability.

For example, to use a custom Dockerfile for OpenShift deployment:

```properties
# Place custom Dockerfiles in the standard location
quarkus.openshift.native-dockerfile=src/main/docker/Dockerfile.custom-native
```

Or for S2I deployment configuration:

```
# Create a standard .s2i/environment file with proper settings
MAVEN_S2I_ARTIFACT_DIRS=target/quarkus-app
S2I_SOURCE_DEPLOYMENTS_FILTER=app lib quarkus quarkus-run.jar
JAVA_OPTIONS=-Dquarkus.http.host=0.0.0.0
JAVA_APP_JAR=/deployments/quarkus-run.jar
```

Using standardized paths improves maintainability and helps team members quickly locate configuration files across different projects. It also prevents confusion when multiple configuration files serve similar purposes but are stored in different locations. Always verify the correct property names when referencing paths (e.g., using `native-dockerfile` for native builds, not `jvm-dockerfile`).