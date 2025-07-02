---
title: Optimize container build configurations
description: Configure containerized application builds to be efficient and flexible
  by avoiding hardcoded architecture decisions and using appropriate compiler flags.
  Let the build system determine architecture targeting instead of maintaining architecture-specific
  code blocks in your Dockerfiles. For Go applications, use appropriate build flags
  like `CGO_ENABLED=0` to...
repository: kubeflow/kubeflow
label: CI/CD
language: Dockerfile
comments_count: 2
repository_stars: 15064
---

Configure containerized application builds to be efficient and flexible by avoiding hardcoded architecture decisions and using appropriate compiler flags. Let the build system determine architecture targeting instead of maintaining architecture-specific code blocks in your Dockerfiles. For Go applications, use appropriate build flags like `CGO_ENABLED=0` to enable static linking and optimize container images.

**Example:**
Instead of:
```dockerfile
RUN if [ "$(uname -m)" = "aarch64" ]; then \
        CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -o webhook -a . ; \
    else \
        CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o webhook -a . ; \
    fi
```

Prefer:
```dockerfile
RUN CGO_ENABLED=0 GOOS=linux go build -o webhook -ldflags "-w" -a .
```

This approach simplifies maintenance, allows multi-architecture builds through tools like Docker buildx (e.g., `docker buildx build --platform linux/amd64,linux/arm64 ...`), and produces more efficient container images.


[
  {
    "discussion_id": "1029353841",
    "pr_number": 6650,
    "pr_file": "components/admission-webhook/Dockerfile",
    "created_at": "2022-11-22T13:51:09+00:00",
    "commented_code": "ENV GO111MODULE=on\n\n# Build\nRUN if [ \"$(uname -m)\" = \"aarch64\" ]; then \\\n        CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -o webhook -a . ; \\\n    else \\\n        CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o webhook -a . ; \\\n    fi\n\nRUN CGO_ENABLED=0 GOOS=linux go build -o webhook -a . ;",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1029353841",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6650,
        "pr_file": "components/admission-webhook/Dockerfile",
        "discussion_id": "1029353841",
        "commented_code": "@@ -10,12 +10,8 @@ COPY . .\n ENV GO111MODULE=on\n \n # Build\n-RUN if [ \"$(uname -m)\" = \"aarch64\" ]; then \\\n-        CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -o webhook -a . ; \\\n-    else \\\n-        CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o webhook -a . ; \\\n-    fi\n-\n+RUN CGO_ENABLED=0 GOOS=linux go build -o webhook -a . ;",
        "comment_created_at": "2022-11-22T13:51:09+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "I understand that by omitting the GOARCH env var we let golang decide on the architecture based on the node environment (machine). \r\n\r\nI'm just trying to wrap my mind around the next step. Is it going to be the process described in https://docs.docker.com/build/building/multi-platform/ to build images that have manifests for different platforms?",
        "pr_file_module": null
      },
      {
        "comment_id": "1029586906",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6650,
        "pr_file": "components/admission-webhook/Dockerfile",
        "discussion_id": "1029353841",
        "commented_code": "@@ -10,12 +10,8 @@ COPY . .\n ENV GO111MODULE=on\n \n # Build\n-RUN if [ \"$(uname -m)\" = \"aarch64\" ]; then \\\n-        CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -o webhook -a . ; \\\n-    else \\\n-        CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o webhook -a . ; \\\n-    fi\n-\n+RUN CGO_ENABLED=0 GOOS=linux go build -o webhook -a . ;",
        "comment_created_at": "2022-11-22T16:41:41+00:00",
        "comment_author": "lehrig",
        "comment_body": "Yes, it's good to let GO determine the arch, so we don't have to maintain an arch list explicitly here or wrap around boiler-plate code with arch-specific if/else statements.\r\n\r\nInstead, we now shift the control which arch is actually build to the build system. If doing nothing special, the arch of the build machine is simply used (and as Kubeflow is currently build on amd64, we are backwards-compatible to the current behavior).\r\n\r\nIn further PRs, we will additionally modify docker-based builds using buildx, where you can, for instance, do something like this:\r\n`docker buildx build --platform linux/amd64,linux/ppc64le ... `\r\n\r\nHere, docker will automatically run actually 2 builds: one for amd64 and one for ppc64le. When coming to above GO-code, GO will acknowledge the external platform configuration and build it correctly. In case no native hardware is available for the given platform, docker will emulate the architecture using QEMU - so you can also build for different archs on amd64.\r\n\r\nThe final outcome is a single multi-arch image with support of all archs listed in Docker's platform statement.",
        "pr_file_module": null
      },
      {
        "comment_id": "1030447960",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6650,
        "pr_file": "components/admission-webhook/Dockerfile",
        "discussion_id": "1029353841",
        "commented_code": "@@ -10,12 +10,8 @@ COPY . .\n ENV GO111MODULE=on\n \n # Build\n-RUN if [ \"$(uname -m)\" = \"aarch64\" ]; then \\\n-        CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -o webhook -a . ; \\\n-    else \\\n-        CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o webhook -a . ; \\\n-    fi\n-\n+RUN CGO_ENABLED=0 GOOS=linux go build -o webhook -a . ;",
        "comment_created_at": "2022-11-23T13:32:16+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "@lehrig this was a *very* thorough explanation of the suggested approach! I'd also suggest to cross post it in the umbrella issue, so that it's readily available for anyone wondering how to e2e approach is going to be.\r\n\r\nAlso LGTM",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "382505839",
    "pr_number": 4775,
    "pr_file": "components/admission-webhook/Dockerfile",
    "created_at": "2020-02-21T10:25:50+00:00",
    "commented_code": "RUN go build  -o webhook .",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "382505839",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 4775,
        "pr_file": "components/admission-webhook/Dockerfile",
        "discussion_id": "382505839",
        "commented_code": "@@ -13,7 +13,7 @@ ENV GO111MODULE=on\n RUN go build  -o webhook .",
        "comment_created_at": "2020-02-21T10:25:50+00:00",
        "comment_author": "swiftdiaries",
        "comment_body": "I think this part is what prevents us from using the static image.\r\n\r\n`CGO_ENABLED=0 GOOS=linux go build -o webook -ldflags \"-w\" -a .`\r\nCould you please try this instead?\r\nWithout `CGO` we should be able to build with static",
        "pr_file_module": null
      },
      {
        "comment_id": "382575357",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 4775,
        "pr_file": "components/admission-webhook/Dockerfile",
        "discussion_id": "382505839",
        "commented_code": "@@ -13,7 +13,7 @@ ENV GO111MODULE=on\n RUN go build  -o webhook .",
        "comment_created_at": "2020-02-21T13:16:47+00:00",
        "comment_author": "jtfogarty",
        "comment_body": "ok, I will test this",
        "pr_file_module": null
      },
      {
        "comment_id": "382592936",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 4775,
        "pr_file": "components/admission-webhook/Dockerfile",
        "discussion_id": "382505839",
        "commented_code": "@@ -13,7 +13,7 @@ ENV GO111MODULE=on\n RUN go build  -o webhook .",
        "comment_created_at": "2020-02-21T13:55:51+00:00",
        "comment_author": "jtfogarty",
        "comment_body": "@swiftdiaries where is that line `CGO_ENABLED=0 GOOS=linux go build -o webook -ldflags \"-w\" -a .` \r\nit's not in the Makefile",
        "pr_file_module": null
      },
      {
        "comment_id": "382685635",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 4775,
        "pr_file": "components/admission-webhook/Dockerfile",
        "discussion_id": "382505839",
        "commented_code": "@@ -13,7 +13,7 @@ ENV GO111MODULE=on\n RUN go build  -o webhook .",
        "comment_created_at": "2020-02-21T16:40:45+00:00",
        "comment_author": "jlewi",
        "comment_body": "I think @swiftdiaries is suggesting changing the existing go-build line to what he provided. I think setting CGO_ENABLED=0 removes a dependency on some c stuff in the compiled binary which might allow the use of static instead of base. ",
        "pr_file_module": null
      },
      {
        "comment_id": "383312620",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 4775,
        "pr_file": "components/admission-webhook/Dockerfile",
        "discussion_id": "382505839",
        "commented_code": "@@ -13,7 +13,7 @@ ENV GO111MODULE=on\n RUN go build  -o webhook .",
        "comment_created_at": "2020-02-24T14:56:26+00:00",
        "comment_author": "krishnadurai",
        "comment_body": "@jeff in the line:\r\n```\r\nRUN CGO_ENABLED=0 GOOS=linux go build -o webook -ldflags \"-w\" -a .\r\n```\r\nWebhook is misspelt.\r\n",
        "pr_file_module": null
      }
    ]
  }
]
