---
title: Structure CI/CD scripts
description: Improve CI/CD shell scripts' readability and maintainability by using
  appropriate shell script patterns. Use heredocs for multiline output generation
  (especially for YAML configurations) and extract repetitive operations into functions.
  This approach reduces duplication, makes scripts easier to understand, and simplifies
  future updates.
repository: chef/chef
label: CI/CD
language: Shell
comments_count: 2
repository_stars: 7860
---

Improve CI/CD shell scripts' readability and maintainability by using appropriate shell script patterns. Use heredocs for multiline output generation (especially for YAML configurations) and extract repetitive operations into functions. This approach reduces duplication, makes scripts easier to understand, and simplifies future updates.

Example 1 - Using heredocs for multiline output:
```bash
# Instead of multiple echo statements:
echo "- label: \":hammer_and_wrench::docker: $platform\""
echo "  retry:"
echo "    automatic:"
# ...many more echo statements...

# Use heredoc syntax:
cat <<- YAML_CONFIG
- label: ":hammer_and_wrench::docker: $platform"
  retry:
    automatic:
      limit: 1
  key: build-$platform
  # ...rest of configuration...
YAML_CONFIG
```

Example 2 - Extracting repetitive operations into functions:
```bash
# Instead of repeating similar commands:
docker manifest create "chef/chef:${CHANNEL}" \
  --amend "chef/chef:${VERSION}-amd64" \
  --amend "chef/chef:${VERSION}-arm64"
docker manifest push "chef/chef:${CHANNEL}"

# Extract into a reusable function:
function create_and_push_manifest() {
  echo "--- Creating manifest for $2"
  docker manifest create "$1:$2" \
    --amend "$1:${EXPEDITOR_VERSION}-amd64" \
    --amend "$1:${EXPEDITOR_VERSION}-arm64"
  
  echo "--- Pushing manifest for $2"
  docker manifest push "$1:$2"
}

# Then call it multiple times:
create_and_push_manifest "chef/chef" "${EXPEDITOR_TARGET_CHANNEL}"
```


[
  {
    "discussion_id": "1082707950",
    "pr_number": 13489,
    "pr_file": ".buildkite/build-test-omnibus.sh",
    "created_at": "2023-01-20T15:35:22+00:00",
    "commented_code": "if [[ $BUILDKITE_ORGANIZATION_SLUG == \"chef-oss\" ]]; then\n  echo \"- block: Build & Test Omnibus Packages\"\n  echo \"  prompt: Continue to run omnibus package build and tests for applicable platforms?\"\nfi\n\nFILTER=\"${OMNIBUS_FILTER:=*}\"\n\nplatforms=(\"amazon-2:centos-7\" \"centos-6:centos-6\" \"centos-7:centos-7\" \"centos-8:centos-8\" \"rhel-9:rhel-9\" \"debian-9:debian-9\" \"debian-10:debian-9\" \"debian-11:debian-9\" \"ubuntu-1604:ubuntu-1604\" \"ubuntu-1804:ubuntu-1604\" \"ubuntu-2004:ubuntu-1604\" \"ubuntu-2204:ubuntu-1604\" \"sles-15:sles-15\" \"windows-2019:windows-2019\")\n\nomnibus_build_platforms=()\nomnibus_test_platforms=()\n\n# build build array and test array based on filter\nfor platform in ${platforms[@]}; do\n    case ${platform%:*} in\n        $FILTER)\n            omnibus_build_platforms[${#omnibus_build_platforms[@]}]=${platform#*:}\n            omnibus_test_platforms[${#omnibus_test_platforms[@]}]=$platform\n            ;;\n    esac\ndone\n\n# remove duplicates from build array\nomnibus_build_platforms=($(printf \"%s\\n\" \"${omnibus_build_platforms[@]}\" | sort -u | tr '\\n' ' '))\n\nfor platform in ${omnibus_build_platforms[@]}; do\n  if [[ $platform != *\"windows\"* ]]; then\n    echo \"- label: \\\":hammer_and_wrench::docker: $platform\\\"\"\n    echo \"  retry:\"\n    echo \"    automatic:\"\n    echo \"      limit: 1\"\n    echo \"  key: build-$platform\"\n    echo \"  agents:\"\n    echo \"    queue: default-privileged\"\n    echo \"  plugins:\"\n    echo \"  - docker#v3.5.0:\"\n    echo \"      image: chefes/omnibus-toolchain-$platform:$OMNIBUS_TOOLCHAIN_VERSION\"\n    echo \"      privileged: true\"\n    echo \"      propagate-environment: true\"\n    echo \"      environment:\"\n    echo \"        - RPM_SIGNING_KEY\"\n    echo \"        - CHEF_FOUNDATION_VERSION\"\n    echo \"  commands:\"\n    echo \"    - ./.expeditor/scripts/omnibus_chef_build.sh\"\n    echo \"  timeout_in_minutes: 60\"\n  else \n    echo \"- label: \\\":hammer_and_wrench::windows: $platform\\\"\"\n    echo \"  retry:\"\n    echo \"    automatic:\"\n    echo \"      limit: 1\"\n    echo \"  key: build-$platform\"\n    echo \"  agents:\"\n    echo \"    queue: default-$platform-privileged\"\n    echo \"  plugins:\"\n    echo \"  - docker#v3.5.0:\"\n    echo \"      image: chefes/omnibus-toolchain-$platform:$OMNIBUS_TOOLCHAIN_VERSION\"\n    echo \"      shell:\"\n    echo \"      - powershell\"\n    echo \"      - \\\"-Command\\\"\"\n    echo \"      propagate-environment: true\"\n    echo \"      environment:\"\n    echo \"        - CHEF_FOUNDATION_VERSION\"\n    echo \"        - BUILDKITE_AGENT_ACCESS_TOKEN\"\n    echo \"        - AWS_ACCESS_KEY_ID\"\n    echo \"        - AWS_SECRET_ACCESS_KEY\"\n    echo \"        - AWS_SESSION_TOKEN\"\n    echo \"      volumes:\"\n    echo '        - \"c:\\\\buildkite-agent:c:\\\\buildkite-agent\"'\n    echo \"  commands:\"\n    echo \"    - ./.expeditor/scripts/omnibus_chef_build.ps1\"\n    echo \"  timeout_in_minutes: 60\"\n  fi\ndone\n\necho \"- wait: ~\"\n\nfor platform in ${omnibus_test_platforms[@]}; do\n  if [[ $platform != *\"windows\"* ]]; then\n    echo \"- env:\"\n    echo \"    OMNIBUS_BUILDER_KEY: build-${platform#*:}\"\n    echo \"  label: \\\":mag::docker: ${platform%:*}\\\"\"\n    echo \"  retry:\"\n    echo \"    automatic:\"\n    echo \"      limit: 1\"\n    echo \"  agents:\"\n    echo \"    queue: default-privileged\"\n    echo \"  plugins:\"\n    echo \"  - docker#v3.5.0:\"\n    echo \"      image: chefes/omnibus-toolchain-${platform%:*}:$OMNIBUS_TOOLCHAIN_VERSION\"\n    echo \"      privileged: true\"\n    echo \"      propagate-environment: true\"\n    echo \"  commands:\"\n    echo \"    - ./.expeditor/scripts/download_built_omnibus_pkgs.sh\"\n    echo \"    - omnibus/omnibus-test.sh\"\n    echo \"  timeout_in_minutes: 60\"\n  else\n    echo \"- env:\"\n    echo \"    OMNIBUS_BUILDER_KEY: build-windows-2019\"\n    echo \"  key: test-windows-2019\"\n    echo '  label: \":mag::windows: windows-2019\"'\n    echo \"  retry:\"\n    echo \"    automatic:\"\n    echo \"      limit: 1\"\n    echo \"  agents:\"\n    echo \"    queue: default-windows-2019-privileged\"\n    echo \"  commands:\"\n    echo \"    - ./.expeditor/scripts/download_built_omnibus_pkgs.ps1\"\n    echo \"    - ./omnibus/omnibus-test.ps1\"\n    echo \"  timeout_in_minutes: 60\"\n  fi\ndone",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "1082707950",
        "repo_full_name": "chef/chef",
        "pr_number": 13489,
        "pr_file": ".buildkite/build-test-omnibus.sh",
        "discussion_id": "1082707950",
        "commented_code": "@@ -0,0 +1,112 @@\n+if [[ $BUILDKITE_ORGANIZATION_SLUG == \"chef-oss\" ]]; then\n+  echo \"- block: Build & Test Omnibus Packages\"\n+  echo \"  prompt: Continue to run omnibus package build and tests for applicable platforms?\"\n+fi\n+\n+FILTER=\"${OMNIBUS_FILTER:=*}\"\n+\n+platforms=(\"amazon-2:centos-7\" \"centos-6:centos-6\" \"centos-7:centos-7\" \"centos-8:centos-8\" \"rhel-9:rhel-9\" \"debian-9:debian-9\" \"debian-10:debian-9\" \"debian-11:debian-9\" \"ubuntu-1604:ubuntu-1604\" \"ubuntu-1804:ubuntu-1604\" \"ubuntu-2004:ubuntu-1604\" \"ubuntu-2204:ubuntu-1604\" \"sles-15:sles-15\" \"windows-2019:windows-2019\")\n+\n+omnibus_build_platforms=()\n+omnibus_test_platforms=()\n+\n+# build build array and test array based on filter\n+for platform in ${platforms[@]}; do\n+    case ${platform%:*} in\n+        $FILTER)\n+            omnibus_build_platforms[${#omnibus_build_platforms[@]}]=${platform#*:}\n+            omnibus_test_platforms[${#omnibus_test_platforms[@]}]=$platform\n+            ;;\n+    esac\n+done\n+\n+# remove duplicates from build array\n+omnibus_build_platforms=($(printf \"%s\\n\" \"${omnibus_build_platforms[@]}\" | sort -u | tr '\\n' ' '))\n+\n+for platform in ${omnibus_build_platforms[@]}; do\n+  if [[ $platform != *\"windows\"* ]]; then\n+    echo \"- label: \\\":hammer_and_wrench::docker: $platform\\\"\"\n+    echo \"  retry:\"\n+    echo \"    automatic:\"\n+    echo \"      limit: 1\"\n+    echo \"  key: build-$platform\"\n+    echo \"  agents:\"\n+    echo \"    queue: default-privileged\"\n+    echo \"  plugins:\"\n+    echo \"  - docker#v3.5.0:\"\n+    echo \"      image: chefes/omnibus-toolchain-$platform:$OMNIBUS_TOOLCHAIN_VERSION\"\n+    echo \"      privileged: true\"\n+    echo \"      propagate-environment: true\"\n+    echo \"      environment:\"\n+    echo \"        - RPM_SIGNING_KEY\"\n+    echo \"        - CHEF_FOUNDATION_VERSION\"\n+    echo \"  commands:\"\n+    echo \"    - ./.expeditor/scripts/omnibus_chef_build.sh\"\n+    echo \"  timeout_in_minutes: 60\"\n+  else \n+    echo \"- label: \\\":hammer_and_wrench::windows: $platform\\\"\"\n+    echo \"  retry:\"\n+    echo \"    automatic:\"\n+    echo \"      limit: 1\"\n+    echo \"  key: build-$platform\"\n+    echo \"  agents:\"\n+    echo \"    queue: default-$platform-privileged\"\n+    echo \"  plugins:\"\n+    echo \"  - docker#v3.5.0:\"\n+    echo \"      image: chefes/omnibus-toolchain-$platform:$OMNIBUS_TOOLCHAIN_VERSION\"\n+    echo \"      shell:\"\n+    echo \"      - powershell\"\n+    echo \"      - \\\"-Command\\\"\"\n+    echo \"      propagate-environment: true\"\n+    echo \"      environment:\"\n+    echo \"        - CHEF_FOUNDATION_VERSION\"\n+    echo \"        - BUILDKITE_AGENT_ACCESS_TOKEN\"\n+    echo \"        - AWS_ACCESS_KEY_ID\"\n+    echo \"        - AWS_SECRET_ACCESS_KEY\"\n+    echo \"        - AWS_SESSION_TOKEN\"\n+    echo \"      volumes:\"\n+    echo '        - \"c:\\\\buildkite-agent:c:\\\\buildkite-agent\"'\n+    echo \"  commands:\"\n+    echo \"    - ./.expeditor/scripts/omnibus_chef_build.ps1\"\n+    echo \"  timeout_in_minutes: 60\"\n+  fi\n+done\n+\n+echo \"- wait: ~\"\n+\n+for platform in ${omnibus_test_platforms[@]}; do\n+  if [[ $platform != *\"windows\"* ]]; then\n+    echo \"- env:\"\n+    echo \"    OMNIBUS_BUILDER_KEY: build-${platform#*:}\"\n+    echo \"  label: \\\":mag::docker: ${platform%:*}\\\"\"\n+    echo \"  retry:\"\n+    echo \"    automatic:\"\n+    echo \"      limit: 1\"\n+    echo \"  agents:\"\n+    echo \"    queue: default-privileged\"\n+    echo \"  plugins:\"\n+    echo \"  - docker#v3.5.0:\"\n+    echo \"      image: chefes/omnibus-toolchain-${platform%:*}:$OMNIBUS_TOOLCHAIN_VERSION\"\n+    echo \"      privileged: true\"\n+    echo \"      propagate-environment: true\"\n+    echo \"  commands:\"\n+    echo \"    - ./.expeditor/scripts/download_built_omnibus_pkgs.sh\"\n+    echo \"    - omnibus/omnibus-test.sh\"\n+    echo \"  timeout_in_minutes: 60\"\n+  else\n+    echo \"- env:\"\n+    echo \"    OMNIBUS_BUILDER_KEY: build-windows-2019\"\n+    echo \"  key: test-windows-2019\"\n+    echo '  label: \":mag::windows: windows-2019\"'\n+    echo \"  retry:\"\n+    echo \"    automatic:\"\n+    echo \"      limit: 1\"\n+    echo \"  agents:\"\n+    echo \"    queue: default-windows-2019-privileged\"\n+    echo \"  commands:\"\n+    echo \"    - ./.expeditor/scripts/download_built_omnibus_pkgs.ps1\"\n+    echo \"    - ./omnibus/omnibus-test.ps1\"\n+    echo \"  timeout_in_minutes: 60\"\n+  fi\n+done",
        "comment_created_at": "2023-01-20T15:35:22+00:00",
        "comment_author": "tpowell-progress",
        "comment_body": "```suggestion\r\nfor platform in ${omnibus_build_platforms[@]}; do\r\n  if [[ $platform != *\"windows\"* ]]; then\r\n    cat <<- NONWINDOWS\r\n- label: \":hammer_and_wrench::docker: $platform\"\r\n  retry:\r\n    automatic:\r\n      limit: 1\r\n  key: build-$platform\r\n  agents:\r\n    queue: default-privileged\r\n  plugins:\r\n  - docker#v3.5.0:\r\n      image: chefes/omnibus-toolchain-$platform:$OMNIBUS_TOOLCHAIN_VERSION\r\n      privileged: true\r\n      propagate-environment: true\r\n      environment:\r\n        - RPM_SIGNING_KEY\r\n        - CHEF_FOUNDATION_VERSION\r\n  commands:\r\n    - ./.expeditor/scripts/omnibus_chef_build.sh\r\n  timeout_in_minutes: 60\r\nNONWINDOWS\r\n  else\r\n    cat <<- WINDOWS\r\n- label: \":hammer_and_wrench::windows: $platform\"\r\n  retry:\r\n    automatic:\r\n      limit: 1\r\n  key: build-$platform\r\n  agents:\r\n    queue: default-$platform-privileged\r\n  plugins:\r\n  - docker#v3.5.0:\r\n      image: chefes/omnibus-toolchain-$platform:$OMNIBUS_TOOLCHAIN_VERSION\r\n      shell:\r\n      - powershell\r\n      - \"-Command\"\r\n      propagate-environment: true\r\n      environment:\r\n        - CHEF_FOUNDATION_VERSION\r\n        - BUILDKITE_AGENT_ACCESS_TOKEN\r\n        - AWS_ACCESS_KEY_ID\r\n        - AWS_SECRET_ACCESS_KEY\r\n        - AWS_SESSION_TOKEN\r\n      volumes:\r\n        - \"c:\\\\buildkite-agent:c:\\\\buildkite-agent\"\r\n  commands:\r\n    - ./.expeditor/scripts/omnibus_chef_build.ps1\r\n  timeout_in_minutes: 60\r\nWINDOWS\r\n  fi\r\ndone\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "678521712",
    "pr_number": 11871,
    "pr_file": ".expeditor/promote-docker-images.sh",
    "created_at": "2021-07-28T17:43:21+00:00",
    "commented_code": "#! /bin/bash\n\n# EXPEDITOR_VERSION exists within the artifact_published workload\n\nexport DOCKER_CLI_EXPERIMENTAL=enabled\n\necho \"--- Creating manifest for ${EXPEDITOR_TARGET_CHANNEL}\"\ndocker manifest create \"chef/chef:${EXPEDITOR_TARGET_CHANNEL}\" \\",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "678521712",
        "repo_full_name": "chef/chef",
        "pr_number": 11871,
        "pr_file": ".expeditor/promote-docker-images.sh",
        "discussion_id": "678521712",
        "commented_code": "@@ -0,0 +1,42 @@\n+#! /bin/bash\n+\n+# EXPEDITOR_VERSION exists within the artifact_published workload\n+\n+export DOCKER_CLI_EXPERIMENTAL=enabled\n+\n+echo \"--- Creating manifest for ${EXPEDITOR_TARGET_CHANNEL}\"\n+docker manifest create \"chef/chef:${EXPEDITOR_TARGET_CHANNEL}\" \\",
        "comment_created_at": "2021-07-28T17:43:21+00:00",
        "comment_author": "mimaslanka",
        "comment_body": "Suggest that we move this to a function\r\n```\r\nfunction create_and_push_manifest ()  {\r\n     echo \"---  Creating...\"\r\n     docker manifest create ${1}:${2}\" \\\r\n         --amend ${1}:${EXPEDITOR_VERSION}-arm64 \\\r\n         --amend ....-amd64\r\n\r\n     echo \"--- Pushing....\"\r\n     docker manifest push....\r\n}\r\ncreate_and_push_manifest \"chef/chef\" \"${EXPEDITOR_TARGET_CHANNEL}\"\r\n \r\nif ....\r\n   create_and_pus_manifest \"chef/chef\" \"latest\"\r\n  ...\r\n```\r\n",
        "pr_file_module": null
      }
    ]
  }
]
