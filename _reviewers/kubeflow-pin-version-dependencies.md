---
title: Pin version dependencies
description: Explicitly pin version dependencies in configuration files to ensure
  reproducible builds and prevent breaking changes. When dealing with external tools,
  scripts, or APIs, always specify exact versions or commit hashes rather than using
  "latest" or master branches.
repository: kubeflow/kubeflow
label: Configurations
language: Other
comments_count: 4
repository_stars: 15064
---

Explicitly pin version dependencies in configuration files to ensure reproducible builds and prevent breaking changes. When dealing with external tools, scripts, or APIs, always specify exact versions or commit hashes rather than using "latest" or master branches.

Examples:
```makefile
# Good: Pin external scripts to specific commit hashes
test -f ${ENVTEST_ASSETS_DIR}/setup-envtest.sh || curl -sSLo ${ENVTEST_ASSETS_DIR}/setup-envtest.sh https://raw.githubusercontent.com/kubernetes-sigs/controller-runtime/a9bd9117a77a2f84bbc546e28991136fe0000dc0/hack/setup-envtest.sh

# Good: Specify exact versions of tools
$(call go-get-tool,$(CONTROLLER_GEN),sigs.k8s.io/controller-tools/cmd/controller-gen@v0.8.0)
```

When managing cross-version compatibility, add clear documentation for when temporary compatibility configurations can be removed:

```yaml
# Good: Document temporary compatibility settings
spec:
  preserveUnknownFields: false # TODO: Remove in Kubeflow 1.7 release
```

For build configurations, explicitly define the environment to ensure consistency:
```makefile
# Setting SHELL to bash allows bash commands to be executed by recipes
SHELL = /usr/bin/env bash -o pipefail
.SHELLFLAGS = -ec
```

Regularly clean up unused dependencies with tools like `go mod tidy` to maintain clean configuration files.
