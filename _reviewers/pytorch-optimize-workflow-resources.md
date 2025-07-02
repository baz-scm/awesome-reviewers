---
title: Optimize workflow resources
description: 'When designing CI/CD workflows, optimize resource usage while maintaining
  appropriate test coverage. Consider these guidelines:


  1. **Avoid duplicate testing configurations** unless explicitly needed'
repository: pytorch/pytorch
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 91169
---

When designing CI/CD workflows, optimize resource usage while maintaining appropriate test coverage. Consider these guidelines:

1. **Avoid duplicate testing configurations** unless explicitly needed
   ```yaml
   # DO: Select one configuration when appropriate
   - name: linux-test-freezing
     if: github.event.schedule == '0 7 * * *' || github.event_name == 'pull_request'
     # Only run one configuration to save resources

   # DON'T: Run redundant configurations that increase resource usage
   - name: linux-test-default
     if: github.event.schedule == '0 7 * * *'
   - name: linux-test-freezing
     if: github.event.schedule == '0 7 * * *'
   ```

2. **Don't over-specify compute resources** unless required for the specific job
   ```yaml
   # DO: Use default runners when sufficient
   jobs:
     build-job:
       runs-on: ubuntu-latest
       # No specific size requirements

   # DON'T: Specify large instances unnecessarily
   jobs:
     build-job:
       runs-on: "linux.12xlarge"  # Only specify if truly needed
   ```

3. **Separate workflow changes logically** to improve review efficiency and maintainability
   - Split CI test changes from dashboard/visualization changes
   - Make smaller, focused PRs that address one concern at a time

This practice ensures cost-effective use of CI/CD resources, faster build times, and more maintainable workflow definitions.


[
  {
    "discussion_id": "2102587511",
    "pr_number": 152298,
    "pr_file": ".github/workflows/inductor-perf-test-nightly-x86.yml",
    "created_at": "2025-05-22T13:37:39+00:00",
    "commented_code": "selected-test-configs: ${{ inputs.benchmark_configs }}\n    secrets: inherit\n\n\n  linux-jammy-cpu-py3_9-gcc11-inductor-test-nightly:\n    name: linux-jammy-cpu-py3.9-gcc11-inductor\n    uses: ./.github/workflows/_linux-test.yml\n    needs: linux-jammy-cpu-py3_9-gcc11-inductor-build\n    if: github.event.schedule == '0 7 * * *'\n    if: github.event.schedule == '0 7 * * *' || github.event_name == 'pull_request'\n    with:\n      build-environment: linux-jammy-py3.9-gcc11-build\n      dashboard-tag: training-false-inference-true-default-true-dynamic-true-cppwrapper-true-aotinductor-true\n      dashboard-tag: training-false-inference-true-default-true-default_freezing-true-dynamic-true-dynamic_freezing-true-cppwrapper-true-cppwrapper_freezing-true-aotinductor-true-aotinductor_freezing-true",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2102587511",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 152298,
        "pr_file": ".github/workflows/inductor-perf-test-nightly-x86.yml",
        "discussion_id": "2102587511",
        "commented_code": "@@ -90,15 +98,14 @@ jobs:\n       selected-test-configs: ${{ inputs.benchmark_configs }}\n     secrets: inherit\n \n-\n   linux-jammy-cpu-py3_9-gcc11-inductor-test-nightly:\n     name: linux-jammy-cpu-py3.9-gcc11-inductor\n     uses: ./.github/workflows/_linux-test.yml\n     needs: linux-jammy-cpu-py3_9-gcc11-inductor-build\n-    if: github.event.schedule == '0 7 * * *'\n+    if: github.event.schedule == '0 7 * * *' || github.event_name == 'pull_request'\n     with:\n       build-environment: linux-jammy-py3.9-gcc11-build\n-      dashboard-tag: training-false-inference-true-default-true-dynamic-true-cppwrapper-true-aotinductor-true\n+      dashboard-tag: training-false-inference-true-default-true-default_freezing-true-dynamic-true-dynamic_freezing-true-cppwrapper-true-cppwrapper_freezing-true-aotinductor-true-aotinductor_freezing-true",
        "comment_created_at": "2025-05-22T13:37:39+00:00",
        "comment_author": "desertfire",
        "comment_body": "Again, all you need to is to add a single `freeing-true` here.",
        "pr_file_module": null
      },
      {
        "comment_id": "2103755948",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 152298,
        "pr_file": ".github/workflows/inductor-perf-test-nightly-x86.yml",
        "discussion_id": "2102587511",
        "commented_code": "@@ -90,15 +98,14 @@ jobs:\n       selected-test-configs: ${{ inputs.benchmark_configs }}\n     secrets: inherit\n \n-\n   linux-jammy-cpu-py3_9-gcc11-inductor-test-nightly:\n     name: linux-jammy-cpu-py3.9-gcc11-inductor\n     uses: ./.github/workflows/_linux-test.yml\n     needs: linux-jammy-cpu-py3_9-gcc11-inductor-build\n-    if: github.event.schedule == '0 7 * * *'\n+    if: github.event.schedule == '0 7 * * *' || github.event_name == 'pull_request'\n     with:\n       build-environment: linux-jammy-py3.9-gcc11-build\n-      dashboard-tag: training-false-inference-true-default-true-dynamic-true-cppwrapper-true-aotinductor-true\n+      dashboard-tag: training-false-inference-true-default-true-default_freezing-true-dynamic-true-dynamic_freezing-true-cppwrapper-true-cppwrapper_freezing-true-aotinductor-true-aotinductor_freezing-true",
        "comment_created_at": "2025-05-23T04:11:10+00:00",
        "comment_author": "LifengWang",
        "comment_body": "Sure. Now I have added a new CI workflow for the tests of the freezing models. So that we can run both the default and the freezing models in the CPU nightly test.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2113851339",
    "pr_number": 152298,
    "pr_file": ".github/workflows/inductor-perf-test-nightly-x86.yml",
    "created_at": "2025-05-29T12:33:16+00:00",
    "commented_code": "monitor-data-collect-interval: 4\n    secrets: inherit\n\n  linux-jammy-cpu-py3_9-gcc11-inductor-test-nightly-freezing:\n    name: linux-jammy-cpu-py3.9-gcc11-inductor\n    uses: ./.github/workflows/_linux-test.yml\n    needs: linux-jammy-cpu-py3_9-gcc11-inductor-build\n    if: github.event.schedule == '0 7 * * *' || github.event_name == 'pull_request'",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2113851339",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 152298,
        "pr_file": ".github/workflows/inductor-perf-test-nightly-x86.yml",
        "discussion_id": "2113851339",
        "commented_code": "@@ -108,6 +115,22 @@ jobs:\n       monitor-data-collect-interval: 4\n     secrets: inherit\n \n+  linux-jammy-cpu-py3_9-gcc11-inductor-test-nightly-freezing:\n+    name: linux-jammy-cpu-py3.9-gcc11-inductor\n+    uses: ./.github/workflows/_linux-test.yml\n+    needs: linux-jammy-cpu-py3_9-gcc11-inductor-build\n+    if: github.event.schedule == '0 7 * * *' || github.event_name == 'pull_request'",
        "comment_created_at": "2025-05-29T12:33:16+00:00",
        "comment_author": "desertfire",
        "comment_body": "This means we will test both freezing ON and OFF every night. Is this really we want here?",
        "pr_file_module": null
      },
      {
        "comment_id": "2113899127",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 152298,
        "pr_file": ".github/workflows/inductor-perf-test-nightly-x86.yml",
        "discussion_id": "2113851339",
        "commented_code": "@@ -108,6 +115,22 @@ jobs:\n       monitor-data-collect-interval: 4\n     secrets: inherit\n \n+  linux-jammy-cpu-py3_9-gcc11-inductor-test-nightly-freezing:\n+    name: linux-jammy-cpu-py3.9-gcc11-inductor\n+    uses: ./.github/workflows/_linux-test.yml\n+    needs: linux-jammy-cpu-py3_9-gcc11-inductor-build\n+    if: github.event.schedule == '0 7 * * *' || github.event_name == 'pull_request'",
        "comment_created_at": "2025-05-29T13:02:31+00:00",
        "comment_author": "LifengWang",
        "comment_body": "Yes, I remember that you mentioned that we need to keep the default test. Maybe we can just run a few tests with freezing off?",
        "pr_file_module": null
      },
      {
        "comment_id": "2114052120",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 152298,
        "pr_file": ".github/workflows/inductor-perf-test-nightly-x86.yml",
        "discussion_id": "2113851339",
        "commented_code": "@@ -108,6 +115,22 @@ jobs:\n       monitor-data-collect-interval: 4\n     secrets: inherit\n \n+  linux-jammy-cpu-py3_9-gcc11-inductor-test-nightly-freezing:\n+    name: linux-jammy-cpu-py3.9-gcc11-inductor\n+    uses: ./.github/workflows/_linux-test.yml\n+    needs: linux-jammy-cpu-py3_9-gcc11-inductor-build\n+    if: github.event.schedule == '0 7 * * *' || github.event_name == 'pull_request'",
        "comment_created_at": "2025-05-29T14:05:01+00:00",
        "comment_author": "desertfire",
        "comment_body": "Did you trigger a dashboard run? Do you have a dashboard link shows how the data is going to be displayed?",
        "pr_file_module": null
      },
      {
        "comment_id": "2115081221",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 152298,
        "pr_file": ".github/workflows/inductor-perf-test-nightly-x86.yml",
        "discussion_id": "2113851339",
        "commented_code": "@@ -108,6 +115,22 @@ jobs:\n       monitor-data-collect-interval: 4\n     secrets: inherit\n \n+  linux-jammy-cpu-py3_9-gcc11-inductor-test-nightly-freezing:\n+    name: linux-jammy-cpu-py3.9-gcc11-inductor\n+    uses: ./.github/workflows/_linux-test.yml\n+    needs: linux-jammy-cpu-py3_9-gcc11-inductor-build\n+    if: github.event.schedule == '0 7 * * *' || github.event_name == 'pull_request'",
        "comment_created_at": "2025-05-30T03:32:34+00:00",
        "comment_author": "LifengWang",
        "comment_body": "Hi @desertfire. I checked the dashboard page for the performance data related to freezing using the following [link](https://hud.pytorch.org/benchmark/compilers) . Set the time range to the last 14 days, precision to AMP, and device to CPU (x86).\r\nIt appears that the freezing test configuration is already included in the dashboard, but no performance data is being displayed.\r\n![image](https://github.com/user-attachments/assets/56df2d1a-1234-4b24-886a-b95e46da0cda)\r\n\r\n\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "2116346509",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 152298,
        "pr_file": ".github/workflows/inductor-perf-test-nightly-x86.yml",
        "discussion_id": "2113851339",
        "commented_code": "@@ -108,6 +115,22 @@ jobs:\n       monitor-data-collect-interval: 4\n     secrets: inherit\n \n+  linux-jammy-cpu-py3_9-gcc11-inductor-test-nightly-freezing:\n+    name: linux-jammy-cpu-py3.9-gcc11-inductor\n+    uses: ./.github/workflows/_linux-test.yml\n+    needs: linux-jammy-cpu-py3_9-gcc11-inductor-build\n+    if: github.event.schedule == '0 7 * * *' || github.event_name == 'pull_request'",
        "comment_created_at": "2025-05-30T17:55:09+00:00",
        "comment_author": "desertfire",
        "comment_body": "OK, I see two problems here:\r\n\r\n1. The landing page of the OSS dashboard defaults to bf16 for inference. If a user selects x86 as the inference backend, they will see an empty page thinking the system is down or something.\r\n2. If you think freezing should be default, we should avoid testing the non-freezing one to cut the hardware expense. Also the names with freezing on is too long which should be fixed.\r\n\r\nUI fixes need to be done in https://github.com/pytorch/test-infra.\r\n\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "2158256290",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 152298,
        "pr_file": ".github/workflows/inductor-perf-test-nightly-x86.yml",
        "discussion_id": "2113851339",
        "commented_code": "@@ -108,6 +115,22 @@ jobs:\n       monitor-data-collect-interval: 4\n     secrets: inherit\n \n+  linux-jammy-cpu-py3_9-gcc11-inductor-test-nightly-freezing:\n+    name: linux-jammy-cpu-py3.9-gcc11-inductor\n+    uses: ./.github/workflows/_linux-test.yml\n+    needs: linux-jammy-cpu-py3_9-gcc11-inductor-build\n+    if: github.event.schedule == '0 7 * * *' || github.event_name == 'pull_request'",
        "comment_created_at": "2025-06-20T07:37:01+00:00",
        "comment_author": "LifengWang",
        "comment_body": "Hi, @desertfire. Now I have removed the non-freezing test, and the test results in the HUD are as follows. Would it make sense to update the CI tests in this PR first, and address the dashboard changes in a follow-up\uff1f\r\n\r\n![image](https://github.com/user-attachments/assets/41762078-2102-4003-b5ee-5fec5c944e65)\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "2167903726",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 152298,
        "pr_file": ".github/workflows/inductor-perf-test-nightly-x86.yml",
        "discussion_id": "2113851339",
        "commented_code": "@@ -108,6 +115,22 @@ jobs:\n       monitor-data-collect-interval: 4\n     secrets: inherit\n \n+  linux-jammy-cpu-py3_9-gcc11-inductor-test-nightly-freezing:\n+    name: linux-jammy-cpu-py3.9-gcc11-inductor\n+    uses: ./.github/workflows/_linux-test.yml\n+    needs: linux-jammy-cpu-py3_9-gcc11-inductor-build\n+    if: github.event.schedule == '0 7 * * *' || github.event_name == 'pull_request'",
        "comment_created_at": "2025-06-26T01:19:13+00:00",
        "comment_author": "LifengWang",
        "comment_body": "Hi, @huydhn, do you have any insights for the dashboard update? Since we want to update the CPU nightly test using the freezing model.",
        "pr_file_module": null
      },
      {
        "comment_id": "2172574300",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 152298,
        "pr_file": ".github/workflows/inductor-perf-test-nightly-x86.yml",
        "discussion_id": "2113851339",
        "commented_code": "@@ -108,6 +115,22 @@ jobs:\n       monitor-data-collect-interval: 4\n     secrets: inherit\n \n+  linux-jammy-cpu-py3_9-gcc11-inductor-test-nightly-freezing:\n+    name: linux-jammy-cpu-py3.9-gcc11-inductor\n+    uses: ./.github/workflows/_linux-test.yml\n+    needs: linux-jammy-cpu-py3_9-gcc11-inductor-build\n+    if: github.event.schedule == '0 7 * * *' || github.event_name == 'pull_request'",
        "comment_created_at": "2025-06-27T18:02:08+00:00",
        "comment_author": "huydhn",
        "comment_body": "Sorry for not seeing your message earlier!  It's ok to land this first and update the dashboard later\r\n\r\ncc @yangw-dev ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2172999953",
    "pr_number": 157181,
    "pr_file": ".github/workflows/h100-symm-mem.yml",
    "created_at": "2025-06-28T00:15:23+00:00",
    "commented_code": "name: Limited CI for symmetric memory tests on H100\n\non:\n  pull_request:\n    paths:\n      - .github/workflows/h100-symm-mem.yml\n  workflow_dispatch:\n  push:\n    tags:\n      - ciflow/h100-symm-mem/*\n  schedule:\n    - cron: 22 8 * * *  # about 1:22am PDT\n\nconcurrency:\n  group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.sha }}-${{ github.event_name == 'workflow_dispatch' }}-${{ github.event_name == 'schedule' }}\n  cancel-in-progress: true\n\njobs:\n\n  get-label-type:\n    if: github.repository_owner == 'pytorch'\n    name: get-label-type\n    uses: pytorch/pytorch/.github/workflows/_runner-determinator.yml@main\n    with:\n      triggering_actor: ${{ github.triggering_actor }}\n      issue_owner: ${{ github.event.pull_request.user.login || github.event.issue.user.login }}\n      curr_branch: ${{ github.head_ref || github.ref_name }}\n      curr_ref_type: ${{ github.ref_type }}\n\n  linux-jammy-cuda12_8-py3_10-gcc11-sm90-build-symm:\n    name: linux-jammy-cuda12.8-py3.10-gcc11-sm90-symm\n    uses: ./.github/workflows/_linux-build.yml\n    needs: get-label-type\n    with:\n      runner_prefix: \"${{ needs.get-label-type.outputs.label-type }}\"\n      runner: \"linux.12xlarge\"",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2172999953",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 157181,
        "pr_file": ".github/workflows/h100-symm-mem.yml",
        "discussion_id": "2172999953",
        "commented_code": "@@ -0,0 +1,55 @@\n+name: Limited CI for symmetric memory tests on H100\n+\n+on:\n+  pull_request:\n+    paths:\n+      - .github/workflows/h100-symm-mem.yml\n+  workflow_dispatch:\n+  push:\n+    tags:\n+      - ciflow/h100-symm-mem/*\n+  schedule:\n+    - cron: 22 8 * * *  # about 1:22am PDT\n+\n+concurrency:\n+  group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.sha }}-${{ github.event_name == 'workflow_dispatch' }}-${{ github.event_name == 'schedule' }}\n+  cancel-in-progress: true\n+\n+jobs:\n+\n+  get-label-type:\n+    if: github.repository_owner == 'pytorch'\n+    name: get-label-type\n+    uses: pytorch/pytorch/.github/workflows/_runner-determinator.yml@main\n+    with:\n+      triggering_actor: ${{ github.triggering_actor }}\n+      issue_owner: ${{ github.event.pull_request.user.login || github.event.issue.user.login }}\n+      curr_branch: ${{ github.head_ref || github.ref_name }}\n+      curr_ref_type: ${{ github.ref_type }}\n+\n+  linux-jammy-cuda12_8-py3_10-gcc11-sm90-build-symm:\n+    name: linux-jammy-cuda12.8-py3.10-gcc11-sm90-symm\n+    uses: ./.github/workflows/_linux-build.yml\n+    needs: get-label-type\n+    with:\n+      runner_prefix: \"${{ needs.get-label-type.outputs.label-type }}\"\n+      runner: \"linux.12xlarge\"",
        "comment_created_at": "2025-06-28T00:15:23+00:00",
        "comment_author": "huydhn",
        "comment_body": "Nit:  I'm not sure why we need `12xlarge` here besides the fact that https://github.com/pytorch/pytorch/blame/main/.github/workflows/h100-distributed.yml also has it.  I don't think you need to set the runner here at all ",
        "pr_file_module": null
      }
    ]
  }
]
