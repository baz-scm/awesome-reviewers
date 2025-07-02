---
title: Precise workflow triggers
description: Configure CI/CD workflows to trigger precisely based on relevant file
  path changes. This minimizes unnecessary builds and tests while ensuring all required
  workflows run when dependencies are modified.
repository: kubeflow/kubeflow
label: CI/CD
language: Yaml
comments_count: 7
repository_stars: 15064
---

Configure CI/CD workflows to trigger precisely based on relevant file path changes. This minimizes unnecessary builds and tests while ensuring all required workflows run when dependencies are modified.

**For component-specific workflows:**
- Include both direct component paths and shared dependencies
- For web applications, include common library paths

```yaml
# Example for a web application workflow
name: Build & Publish JWA Docker image
on:
  push:
    branches:
      - master
      - v*-branch
    paths:
      - components/crud-web-apps/jupyter/**      # Component code
      - components/crud-web-apps/common/**       # Shared dependencies
```

**For manifest-related workflows:**
- Target only specific manifest directories rather than all component files

```yaml
# For manifest testing, specify manifest paths only
name: Build Profile Controller manifests
on:
  pull_request:
    paths:
      - components/profile-controller/config/**  # Only manifest changes
```

Centralize build logic in Makefiles instead of duplicating in GitHub Actions. This allows workflows to simply call make targets, making pipelines more maintainable and consistent across environments.


[
  {
    "discussion_id": "1053079365",
    "pr_number": 6854,
    "pr_file": ".github/workflows/centraldb_angular_docker_publish.yaml",
    "created_at": "2022-12-20T09:16:52+00:00",
    "commented_code": "id: version\n      if: steps.filter.outputs.version == 'true'\n      run: |\n        docker tag ${{env.IMG}}:${TAG} ${{env.IMG}}:${VERSION_TAG}\n        export VERSION_TAG=$(cat releasing/version/VERSION)\n        docker tag ${{env.IMG}}:${{env.TAG}} ${{env.IMG}}:${VERSION_TAG}\n        docker push ${{env.IMG}}:${VERSION_TAG}",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1053079365",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6854,
        "pr_file": ".github/workflows/centraldb_angular_docker_publish.yaml",
        "discussion_id": "1053079365",
        "commented_code": "@@ -49,8 +50,6 @@ jobs:\n       id: version\n       if: steps.filter.outputs.version == 'true'\n       run: |\n-        docker tag ${{env.IMG}}:${TAG} ${{env.IMG}}:${VERSION_TAG}\n+        export VERSION_TAG=$(cat releasing/version/VERSION)\n+        docker tag ${{env.IMG}}:${{env.TAG}} ${{env.IMG}}:${VERSION_TAG}\n         docker push ${{env.IMG}}:${VERSION_TAG}",
        "comment_created_at": "2022-12-20T09:16:52+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "Let's re-use the makefile rules here, to avoid duplication of code in makefiles and GH Actions. The layers are already cached so rebuilding the image should be very fast\r\n```bash\r\nexport TAG=$(cat releasing/version/VERSION)\r\ncd components/centraldashboard-angular\r\nmake docker-build docker-push\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1053177606",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6854,
        "pr_file": ".github/workflows/centraldb_angular_docker_publish.yaml",
        "discussion_id": "1053079365",
        "commented_code": "@@ -49,8 +50,6 @@ jobs:\n       id: version\n       if: steps.filter.outputs.version == 'true'\n       run: |\n-        docker tag ${{env.IMG}}:${TAG} ${{env.IMG}}:${VERSION_TAG}\n+        export VERSION_TAG=$(cat releasing/version/VERSION)\n+        docker tag ${{env.IMG}}:${{env.TAG}} ${{env.IMG}}:${VERSION_TAG}\n         docker push ${{env.IMG}}:${VERSION_TAG}",
        "comment_created_at": "2022-12-20T10:48:13+00:00",
        "comment_author": "apo-ger",
        "comment_body": "Sure! However, we can't avoid duplication of code for building/pushing the notebook server images. This is because we don't have an `IMG` env var in the Makefiles (e.g [codeserver-python Makefile](https://github.com/kubeflow/kubeflow/blob/658f5b8a76e3b19438678decaf21a9c2fdfd9af1/components/example-notebook-servers/codeserver-python/Makefile#L1)) to set the `registry` there. Therefore with the current Makefiles we have to use:\r\n- `make docker-build`\r\n- `docker tag` to add the registry\r\n- and finally `docker push`\r\n\r\nFor example:\r\n```yaml\r\n    - name: Build and push Notebook Server images\r\n      run: |\r\n        export TAG=$(shell git describe --tags --always --dirty)\r\n        cd components/example-notebook-servers/\r\n        make docker-build -C codeserver-python TAG=${TAG}\r\n        docker tag codeserver-python:${TAG} ${{env.REGISTRY}}/codeserver-python:${TAG}\r\n        docker push ${{env.REGISTRY}}/codeserver-python:${TAG}\r\n\r\n    - name: Build and push latest Notebook Server images\r\n      if: github.ref == 'refs/heads/master'\r\n      run: |  \r\n        export TAG=latest\r\n        cd components/example-notebook-servers/\r\n        make docker-build -C codeserver-python TAG=${TAG}\r\n        docker tag codeserver-python:${TAG} ${{env.REGISTRY}}/codeserver-python:${TAG}\r\n        docker push ${{env.REGISTRY}}/codeserver-python:${TAG}\r\n\r\n    - name: Build and push Notebook Server images on Version change\r\n      id: version\r\n      if: steps.filter.outputs.version == 'true'\r\n      run: |\r\n        export TAG=$(cat releasing/version/VERSION)\r\n        cd components/example-notebook-servers/\r\n        make docker-build -C codeserver-python TAG=${TAG}\r\n        docker tag codeserver-python:${TAG} ${{env.REGISTRY}}/codeserver-python:${TAG}\r\n        docker push ${{env.REGISTRY}}/codeserver-python:${TAG}\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1053230770",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6854,
        "pr_file": ".github/workflows/centraldb_angular_docker_publish.yaml",
        "discussion_id": "1053079365",
        "commented_code": "@@ -49,8 +50,6 @@ jobs:\n       id: version\n       if: steps.filter.outputs.version == 'true'\n       run: |\n-        docker tag ${{env.IMG}}:${TAG} ${{env.IMG}}:${VERSION_TAG}\n+        export VERSION_TAG=$(cat releasing/version/VERSION)\n+        docker tag ${{env.IMG}}:${{env.TAG}} ${{env.IMG}}:${VERSION_TAG}\n         docker push ${{env.IMG}}:${VERSION_TAG}",
        "comment_created_at": "2022-12-20T11:49:53+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "@apo-ger let's leave the notebook images completely out for this effort.\r\n\r\nI believe we would be able to use the Makefiles if we'd use a `REGISTRY` env var in each Makefile. But let's discuss this in a follow up PR, since this one is already getting big",
        "pr_file_module": null
      },
      {
        "comment_id": "1053247283",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6854,
        "pr_file": ".github/workflows/centraldb_angular_docker_publish.yaml",
        "discussion_id": "1053079365",
        "commented_code": "@@ -49,8 +50,6 @@ jobs:\n       id: version\n       if: steps.filter.outputs.version == 'true'\n       run: |\n-        docker tag ${{env.IMG}}:${TAG} ${{env.IMG}}:${VERSION_TAG}\n+        export VERSION_TAG=$(cat releasing/version/VERSION)\n+        docker tag ${{env.IMG}}:${{env.TAG}} ${{env.IMG}}:${VERSION_TAG}\n         docker push ${{env.IMG}}:${VERSION_TAG}",
        "comment_created_at": "2022-12-20T12:10:38+00:00",
        "comment_author": "apo-ger",
        "comment_body": "@kimwnasptd \r\n> let's leave the notebook images completely out for this effort.\r\n\r\nShould I remove the logic for building/pushing with latest tag or remove the notebook-server workflows completely and tackle them in the follow up PR (manifests/Makefiles/workflows)?",
        "pr_file_module": null
      },
      {
        "comment_id": "1053260293",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6854,
        "pr_file": ".github/workflows/centraldb_angular_docker_publish.yaml",
        "discussion_id": "1053079365",
        "commented_code": "@@ -49,8 +50,6 @@ jobs:\n       id: version\n       if: steps.filter.outputs.version == 'true'\n       run: |\n-        docker tag ${{env.IMG}}:${TAG} ${{env.IMG}}:${VERSION_TAG}\n+        export VERSION_TAG=$(cat releasing/version/VERSION)\n+        docker tag ${{env.IMG}}:${{env.TAG}} ${{env.IMG}}:${VERSION_TAG}\n         docker push ${{env.IMG}}:${VERSION_TAG}",
        "comment_created_at": "2022-12-20T12:26:10+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "just the changes from this PR, and we can send another PR for the latest tag in a separate PR that:\r\n1. Uses a `REGISTRY` env var in all makefiles (let's see if we need to do more)\r\n2. Use the Makefiles to build each notebook, but with a different TAG each time like we do for the rest of the components",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "900127527",
    "pr_number": 6524,
    "pr_file": ".github/workflows/centraldb_manifests_build.yaml",
    "created_at": "2022-06-17T13:39:53+00:00",
    "commented_code": "name: Build CentralDashboard manifests\non:\n  pull_request:\n    paths:\n      - components/centraldashboard/**",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "900127527",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6524,
        "pr_file": ".github/workflows/centraldb_manifests_build.yaml",
        "discussion_id": "900127527",
        "commented_code": "@@ -0,0 +1,23 @@\n+name: Build CentralDashboard manifests\n+on:\n+  pull_request:\n+    paths:\n+      - components/centraldashboard/**",
        "comment_created_at": "2022-06-17T13:39:53+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "Since we are testing manifests this time we don't want to trigger the workflows when code changes, but rather when the **manifests** change.\r\n\r\nSo in this case it will be `components/centraldashboard/manifests/**`",
        "pr_file_module": null
      },
      {
        "comment_id": "900190123",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6524,
        "pr_file": ".github/workflows/centraldb_manifests_build.yaml",
        "discussion_id": "900127527",
        "commented_code": "@@ -0,0 +1,23 @@\n+name: Build CentralDashboard manifests\n+on:\n+  pull_request:\n+    paths:\n+      - components/centraldashboard/**",
        "comment_created_at": "2022-06-17T14:44:05+00:00",
        "comment_author": "NickLoukas",
        "comment_body": "I made the change.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "900197491",
    "pr_number": 6524,
    "pr_file": ".github/workflows/prof_controller_manifests_test.yaml",
    "created_at": "2022-06-17T14:52:02+00:00",
    "commented_code": "name: Build Profile Controller manifests\non:\n  pull_request:\n    paths:\n      - components/profile-controller/**",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "900197491",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6524,
        "pr_file": ".github/workflows/prof_controller_manifests_test.yaml",
        "discussion_id": "900197491",
        "commented_code": "@@ -0,0 +1,23 @@\n+name: Build Profile Controller manifests\n+on:\n+  pull_request:\n+    paths:\n+      - components/profile-controller/**",
        "comment_created_at": "2022-06-17T14:52:02+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "I think you missed this one. It should be `components/profile-controller/config/**`",
        "pr_file_module": null
      },
      {
        "comment_id": "900214466",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6524,
        "pr_file": ".github/workflows/prof_controller_manifests_test.yaml",
        "discussion_id": "900197491",
        "commented_code": "@@ -0,0 +1,23 @@\n+name: Build Profile Controller manifests\n+on:\n+  pull_request:\n+    paths:\n+      - components/profile-controller/**",
        "comment_created_at": "2022-06-17T15:10:07+00:00",
        "comment_author": "NickLoukas",
        "comment_body": "Yeap you are correct. Fixed it.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "893852939",
    "pr_number": 6510,
    "pr_file": ".github/workflows/jwa_docker_publish.yaml",
    "created_at": "2022-06-09T18:51:06+00:00",
    "commented_code": "name: Build & Publish JWA Docker image\non:\n  push:\n    branches:\n      - master\n      - v*-branch\n    paths:\n      - components/crud-web-apps/jupyter/**",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "893852939",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6510,
        "pr_file": ".github/workflows/jwa_docker_publish.yaml",
        "discussion_id": "893852939",
        "commented_code": "@@ -0,0 +1,28 @@\n+name: Build & Publish JWA Docker image\n+on:\n+  push:\n+    branches:\n+      - master\n+      - v*-branch\n+    paths:\n+      - components/crud-web-apps/jupyter/**",
        "comment_created_at": "2022-06-09T18:51:06+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "Lets add another path here for `components/crud-web-apps/common/**`. We want the web app to be rebuild whenever we also touch the common code.",
        "pr_file_module": null
      },
      {
        "comment_id": "894351947",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6510,
        "pr_file": ".github/workflows/jwa_docker_publish.yaml",
        "discussion_id": "893852939",
        "commented_code": "@@ -0,0 +1,28 @@\n+name: Build & Publish JWA Docker image\n+on:\n+  push:\n+    branches:\n+      - master\n+      - v*-branch\n+    paths:\n+      - components/crud-web-apps/jupyter/**",
        "comment_created_at": "2022-06-10T09:45:07+00:00",
        "comment_author": "NickLoukas",
        "comment_body": "Added that.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "893857912",
    "pr_number": 6510,
    "pr_file": ".github/workflows/twa_docker_publish.yaml",
    "created_at": "2022-06-09T18:57:27+00:00",
    "commented_code": "name: Build & Publish TWA Docker image\non:\n  push:\n    branches:\n      - master\n      - v*-branch\n    paths:\n      - components/crud-web-apps/tensorboards/**",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "893857912",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6510,
        "pr_file": ".github/workflows/twa_docker_publish.yaml",
        "discussion_id": "893857912",
        "commented_code": "@@ -0,0 +1,28 @@\n+name: Build & Publish TWA Docker image\n+on:\n+  push:\n+    branches:\n+      - master\n+      - v*-branch\n+    paths:\n+      - components/crud-web-apps/tensorboards/**",
        "comment_created_at": "2022-06-09T18:57:27+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "Lets add another path here for `components/crud-web-apps/common/**`. We want the web app to be rebuild whenever we also touch the common code.",
        "pr_file_module": null
      },
      {
        "comment_id": "894352668",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6510,
        "pr_file": ".github/workflows/twa_docker_publish.yaml",
        "discussion_id": "893857912",
        "commented_code": "@@ -0,0 +1,28 @@\n+name: Build & Publish TWA Docker image\n+on:\n+  push:\n+    branches:\n+      - master\n+      - v*-branch\n+    paths:\n+      - components/crud-web-apps/tensorboards/**",
        "comment_created_at": "2022-06-10T09:46:00+00:00",
        "comment_author": "NickLoukas",
        "comment_body": "Added that.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "893858030",
    "pr_number": 6510,
    "pr_file": ".github/workflows/vwa_docker_publish.yaml",
    "created_at": "2022-06-09T18:57:35+00:00",
    "commented_code": "name: Build & Publish VWA Docker image\non:\n  push:\n    branches:\n      - master\n      - v*-branch\n    paths:\n      - components/crud-web-apps/volumes/**",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "893858030",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6510,
        "pr_file": ".github/workflows/vwa_docker_publish.yaml",
        "discussion_id": "893858030",
        "commented_code": "@@ -0,0 +1,28 @@\n+name: Build & Publish VWA Docker image\n+on:\n+  push:\n+    branches:\n+      - master\n+      - v*-branch\n+    paths:\n+      - components/crud-web-apps/volumes/**",
        "comment_created_at": "2022-06-09T18:57:35+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "Lets add another path here for `components/crud-web-apps/common/**`. We want the web app to be rebuild whenever we also touch the common code.",
        "pr_file_module": null
      },
      {
        "comment_id": "894352798",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6510,
        "pr_file": ".github/workflows/vwa_docker_publish.yaml",
        "discussion_id": "893858030",
        "commented_code": "@@ -0,0 +1,28 @@\n+name: Build & Publish VWA Docker image\n+on:\n+  push:\n+    branches:\n+      - master\n+      - v*-branch\n+    paths:\n+      - components/crud-web-apps/volumes/**",
        "comment_created_at": "2022-06-10T09:46:10+00:00",
        "comment_author": "NickLoukas",
        "comment_body": "Added that.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "893898341",
    "pr_number": 6510,
    "pr_file": ".github/workflows/nb_controller_docker_publish.yaml",
    "created_at": "2022-06-09T19:50:43+00:00",
    "commented_code": "name: Build & Publish Notebook Controller Docker image\non:\n  push:\n    branches:\n      - master\n      - v*-branch\n    paths:\n      - components/notebook-controller/**",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "893898341",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6510,
        "pr_file": ".github/workflows/nb_controller_docker_publish.yaml",
        "discussion_id": "893898341",
        "commented_code": "@@ -0,0 +1,30 @@\n+name: Build & Publish Notebook Controller Docker image\n+on:\n+  push:\n+    branches:\n+      - master\n+      - v*-branch\n+    paths:\n+      - components/notebook-controller/**",
        "comment_created_at": "2022-06-09T19:50:43+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "Let's also trigger this workflow for the `/components/common/**` directory, since it's using common code from there",
        "pr_file_module": null
      },
      {
        "comment_id": "894353026",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6510,
        "pr_file": ".github/workflows/nb_controller_docker_publish.yaml",
        "discussion_id": "893898341",
        "commented_code": "@@ -0,0 +1,30 @@\n+name: Build & Publish Notebook Controller Docker image\n+on:\n+  push:\n+    branches:\n+      - master\n+      - v*-branch\n+    paths:\n+      - components/notebook-controller/**",
        "comment_created_at": "2022-06-10T09:46:28+00:00",
        "comment_author": "NickLoukas",
        "comment_body": "Added that.",
        "pr_file_module": null
      }
    ]
  }
]
