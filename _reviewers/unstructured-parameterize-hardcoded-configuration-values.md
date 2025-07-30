---
title: Parameterize hardcoded configuration values
description: Replace hardcoded values in configuration files with parameterized variables
  to improve flexibility and maintainability. Use build arguments (ARG) and environment
  variables (ENV) in Dockerfiles instead of embedding specific versions, paths, or
  other configuration values directly in the code.
repository: Unstructured-IO/unstructured
label: Configurations
language: Dockerfile
comments_count: 2
repository_stars: 12117
---

Replace hardcoded values in configuration files with parameterized variables to improve flexibility and maintainability. Use build arguments (ARG) and environment variables (ENV) in Dockerfiles instead of embedding specific versions, paths, or other configuration values directly in the code.

This approach makes configurations more adaptable to different environments and reduces the need to modify multiple locations when values change. For example, instead of hardcoding tool versions and paths throughout a Dockerfile:

```dockerfile
# Instead of hardcoded values:
RUN pip3.11 install --user -r requirements.txt
COPY ./nltk_data /home/notebook-user/nltk_data

# Use parameterized approach:
ARG PYTHON_VERSION=3.11
ARG NLTK_DATA_SOURCE=./nltk_data
ENV PIP=pip${PYTHON_VERSION}

RUN ${PIP} install --user -r requirements.txt
COPY ${NLTK_DATA_SOURCE} /home/notebook-user/nltk_data
```

This pattern applies to any configuration file where values might need to change across different environments or deployments.