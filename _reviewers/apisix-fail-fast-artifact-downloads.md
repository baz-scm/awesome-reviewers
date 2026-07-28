---
title: Fail-fast artifact downloads
description: For required build/CI artifacts, make the reference configurable (with
  a sensible default) and fetch them with fail-fast settings so HTTP errors, missing
  files, or bad refs stop the build immediately.
repository: apache/apisix
label: Error Handling
language: Shell
comments_count: 2
repository_stars: 16922
---

For required build/CI artifacts, make the reference configurable (with a sensible default) and fetch them with fail-fast settings so HTTP errors, missing files, or bad refs stop the build immediately.

Apply this rule by:
- Defining the artifact ref via an environment variable with a fallback.
- Using `curl -fsSL` for downloads (fail on HTTP errors, show errors, follow redirects as needed), and avoid commands that allow silent/partial failures.

Example pattern:
```sh
APISIX_BUILD_TOOLS_REF="${APISIX_BUILD_TOOLS_REF:-apisix-runtime/${APISIX_RUNTIME}}"

curl -fsSL -o /usr/local/openresty/openssl3/ssl/openssl.cnf \
  "https://raw.githubusercontent.com/api7/apisix-build-tools/${APISIX_BUILD_TOOLS_REF}/conf/openssl3/openssl.cnf"
```
This improves error handling by ensuring failure scenarios (missing artifact, incorrect ref, HTTP 404/500) are detected and propagated immediately rather than producing misleading downstream errors.