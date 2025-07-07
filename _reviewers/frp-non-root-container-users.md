---
title: Non-root container users
description: Always run containers with a non-root user to reduce the security attack
  surface. Modern Docker allows non-root users to bind to privileged ports (80, 443),
  eliminating a common reason for using root. Create a dedicated user and group in
  your Dockerfile and ensure your application runs with that user's privileges.
repository: fatedier/frp
label: Security
language: Dockerfile
comments_count: 1
repository_stars: 95938
---

Always run containers with a non-root user to reduce the security attack surface. Modern Docker allows non-root users to bind to privileged ports (80, 443), eliminating a common reason for using root. Create a dedicated user and group in your Dockerfile and ensure your application runs with that user's privileges.

Example:
```Dockerfile
FROM alpine:3.18 AS runtime

ARG APP
# Create a non-root user and group
RUN addgroup -g 1000 -S ${APP} && \
    adduser -u 1000 -S ${APP} -G ${APP} --home /app

# Set the working directory owned by the non-root user
WORKDIR /app
COPY --from=builder /building/bin/${APP} /app/

# Switch to non-root user
USER ${APP}

# Run the application
CMD ["/app/your-application"]
```