---
title: Externalize configuration values
description: Avoid hardcoding configuration values directly in scripts, especially
  for values that might change between environments or contain sensitive information.
  Instead, use environment variables, build parameters, or secrets management systems.
repository: chef/chef
label: Configurations
language: Shell
comments_count: 6
repository_stars: 7860
---

Avoid hardcoding configuration values directly in scripts, especially for values that might change between environments or contain sensitive information. Instead, use environment variables, build parameters, or secrets management systems.

Key practices:
1. Move endpoint URLs, license keys, and service addresses to environment variables
2. Maintain consistent naming conventions for environment variables across different scripts
3. Configure CI/CD systems to inject these values during build and deployment
4. Use default values only for development environments, never for production configurations

Example - Instead of:
```bash
export CHEF_LICENSE_SERVER="http://hosted-license-service-lb-8000-606952349.us-west-2.elb.amazonaws.com:8000"
```

Use:
```bash
export CHEF_LICENSE_SERVER="${CHEF_LICENSE_SERVER:-fallback_value_for_dev_only}"
```

Or configure the value in your CI/CD system's environment variables or secrets store.

For version information, prefer environment variables provided by your CI/CD system over reading from files:
```bash
# Preferred
VERSION="${EXPEDITOR_VERSION}"

# Avoid
VERSION=$(cat VERSION)
```


[
  {
    "discussion_id": "1713904952",
    "pr_number": 14467,
    "pr_file": ".expeditor/scripts/bk_container_prep.sh",
    "created_at": "2024-08-12T14:34:36+00:00",
    "commented_code": "export FORCE_FFI_YAJL=\"ext\"\nexport CHEF_LICENSE=\"accept-no-persist\"\nexport ENV[\"CHEF_LICENSE_SERVER\"] = \"http://hosted-license-service-lb-8000-606952349.us-west-2.elb.amazonaws.com:8000/\"",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "1713904952",
        "repo_full_name": "chef/chef",
        "pr_number": 14467,
        "pr_file": ".expeditor/scripts/bk_container_prep.sh",
        "discussion_id": "1713904952",
        "commented_code": "@@ -18,6 +18,8 @@ echo \"--- Preparing Container...\"\n \n export FORCE_FFI_YAJL=\"ext\"\n export CHEF_LICENSE=\"accept-no-persist\"\n+export ENV[\"CHEF_LICENSE_SERVER\"] = \"http://hosted-license-service-lb-8000-606952349.us-west-2.elb.amazonaws.com:8000/\"",
        "comment_created_at": "2024-08-12T14:34:36+00:00",
        "comment_author": "tpowell-progress",
        "comment_body": "Feels like these env vars should be set in Buildkite itself.",
        "pr_file_module": null
      },
      {
        "comment_id": "1714794576",
        "repo_full_name": "chef/chef",
        "pr_number": 14467,
        "pr_file": ".expeditor/scripts/bk_container_prep.sh",
        "discussion_id": "1713904952",
        "commented_code": "@@ -18,6 +18,8 @@ echo \"--- Preparing Container...\"\n \n export FORCE_FFI_YAJL=\"ext\"\n export CHEF_LICENSE=\"accept-no-persist\"\n+export ENV[\"CHEF_LICENSE_SERVER\"] = \"http://hosted-license-service-lb-8000-606952349.us-west-2.elb.amazonaws.com:8000/\"",
        "comment_created_at": "2024-08-13T07:18:59+00:00",
        "comment_author": "ahasunos",
        "comment_body": "will refactor them to be in a single place instead of spread out throughout the codebase.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1743781220",
    "pr_number": 14467,
    "pr_file": ".expeditor/scripts/bk_container_prep.sh",
    "created_at": "2024-09-04T13:18:55+00:00",
    "commented_code": "export FORCE_FFI_YAJL=\"ext\"\nexport CHEF_LICENSE=\"accept-no-persist\"\nexport CHEF_LICENSE_SERVER=\"http://hosted-license-service-lb-8000-606952349.us-west-2.elb.amazonaws.com:8000\"",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "1743781220",
        "repo_full_name": "chef/chef",
        "pr_number": 14467,
        "pr_file": ".expeditor/scripts/bk_container_prep.sh",
        "discussion_id": "1743781220",
        "commented_code": "@@ -18,6 +18,8 @@ echo \"--- Preparing Container...\"\n \n export FORCE_FFI_YAJL=\"ext\"\n export CHEF_LICENSE=\"accept-no-persist\"\n+export CHEF_LICENSE_SERVER=\"http://hosted-license-service-lb-8000-606952349.us-west-2.elb.amazonaws.com:8000\"",
        "comment_created_at": "2024-09-04T13:18:55+00:00",
        "comment_author": "tpowell-progress",
        "comment_body": "We don't need to be pointing at a raw endpoint in the code. It's likely unstable, and we probably don't want to expose it, regardless. Needs to be injected via secrets or env just to not have to have a pull request (that will have failing pipelines due to this value being stale) to update this value.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1743784377",
    "pr_number": 14467,
    "pr_file": ".expeditor/scripts/bk_linux_exec.sh",
    "created_at": "2024-09-04T13:20:33+00:00",
    "commented_code": "export BUNDLE_GEMFILE=$PWD/kitchen-tests/Gemfile\nexport FORCE_FFI_YAJL=ext\nexport CHEF_LICENSE=\"accept-silent\"\nexport CHEF_LICENSE_SERVER=\"http://hosted-license-service-lb-8000-606952349.us-west-2.elb.amazonaws.com:8000\"",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "1743784377",
        "repo_full_name": "chef/chef",
        "pr_number": 14467,
        "pr_file": ".expeditor/scripts/bk_linux_exec.sh",
        "discussion_id": "1743784377",
        "commented_code": "@@ -28,6 +28,8 @@ asdf global ruby $ruby_version\n export BUNDLE_GEMFILE=$PWD/kitchen-tests/Gemfile\n export FORCE_FFI_YAJL=ext\n export CHEF_LICENSE=\"accept-silent\"\n+export CHEF_LICENSE_SERVER=\"http://hosted-license-service-lb-8000-606952349.us-west-2.elb.amazonaws.com:8000\"",
        "comment_created_at": "2024-09-04T13:20:33+00:00",
        "comment_author": "tpowell-progress",
        "comment_body": "Secrets / env value instead of statically defined in code.\r\n",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1743784601",
    "pr_number": 14467,
    "pr_file": ".expeditor/scripts/prep_and_run_tests.sh",
    "created_at": "2024-09-04T13:20:40+00:00",
    "commented_code": "set -euo pipefail\n\nexport CHEF_LICENSE_SERVER=\"http://hosted-license-service-lb-8000-606952349.us-west-2.elb.amazonaws.com:8000/\"",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "1743784601",
        "repo_full_name": "chef/chef",
        "pr_number": 14467,
        "pr_file": ".expeditor/scripts/prep_and_run_tests.sh",
        "discussion_id": "1743784601",
        "commented_code": "@@ -2,6 +2,8 @@\n \n set -euo pipefail\n \n+export CHEF_LICENSE_SERVER=\"http://hosted-license-service-lb-8000-606952349.us-west-2.elb.amazonaws.com:8000/\"",
        "comment_created_at": "2024-09-04T13:20:40+00:00",
        "comment_author": "tpowell-progress",
        "comment_body": "Secrets / env value instead of statically defined in code.\r\n",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1903930493",
    "pr_number": 14775,
    "pr_file": ".expeditor/scripts/build-infra-deb.sh",
    "created_at": "2025-01-06T09:45:12+00:00",
    "commented_code": "#!/bin/bash\n\nset -euo pipefail\n\nvalidate_env_vars() {\n    if [ -z \"${CHEF_INFRA_MIGRATE_TAR_DEB:-}\" ] || [ -z \"${CHEF_INFRA_HAB_TAR_DEB:-}\" ]; then",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "1903930493",
        "repo_full_name": "chef/chef",
        "pr_number": 14775,
        "pr_file": ".expeditor/scripts/build-infra-deb.sh",
        "discussion_id": "1903930493",
        "commented_code": "@@ -0,0 +1,187 @@\n+#!/bin/bash\n+\n+set -euo pipefail\n+\n+validate_env_vars() {\n+    if [ -z \"${CHEF_INFRA_MIGRATE_TAR_DEB:-}\" ] || [ -z \"${CHEF_INFRA_HAB_TAR_DEB:-}\" ]; then",
        "comment_created_at": "2025-01-06T09:45:12+00:00",
        "comment_author": "sajjaphani",
        "comment_body": "Remove `_DEB` from the environment variable to align with the other build script for RPM.\r\n",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "678445053",
    "pr_number": 11871,
    "pr_file": ".expeditor/promote-docker-images.sh",
    "created_at": "2021-07-28T16:01:22+00:00",
    "commented_code": "#! /bin/bash\n\nexport DOCKER_CLI_EXPERIMENTAL=enabled\n\nVERSION=$(cat VERSION)",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "678445053",
        "repo_full_name": "chef/chef",
        "pr_number": 11871,
        "pr_file": ".expeditor/promote-docker-images.sh",
        "discussion_id": "678445053",
        "commented_code": "@@ -0,0 +1,42 @@\n+#! /bin/bash\n+\n+export DOCKER_CLI_EXPERIMENTAL=enabled\n+\n+VERSION=$(cat VERSION)",
        "comment_created_at": "2021-07-28T16:01:22+00:00",
        "comment_author": "jeremiahsnapp",
        "comment_body": "I don't think you want the contents of the VERSION file. Those contents could be different from the version that is being promoted. I think you can just have this script use `EXPEDITOR_VERSION`.",
        "pr_file_module": null
      },
      {
        "comment_id": "678468868",
        "repo_full_name": "chef/chef",
        "pr_number": 11871,
        "pr_file": ".expeditor/promote-docker-images.sh",
        "discussion_id": "678445053",
        "commented_code": "@@ -0,0 +1,42 @@\n+#! /bin/bash\n+\n+export DOCKER_CLI_EXPERIMENTAL=enabled\n+\n+VERSION=$(cat VERSION)",
        "comment_created_at": "2021-07-28T16:31:33+00:00",
        "comment_author": "nkierpiec",
        "comment_body": "Ah, yea - the whole head of promotion thing would make this a problem - good catch",
        "pr_file_module": null
      }
    ]
  }
]
