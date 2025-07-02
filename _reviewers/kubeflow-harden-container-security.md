---
title: Harden container security
description: 'When building container images, ensure they''re compatible with restricted
  Kubernetes security contexts. Use numeric UIDs instead of symbolic usernames, and
  test compatibility with the following security constraints:'
repository: kubeflow/kubeflow
label: Security
language: Dockerfile
comments_count: 1
repository_stars: 15064
---

When building container images, ensure they're compatible with restricted Kubernetes security contexts. Use numeric UIDs instead of symbolic usernames, and test compatibility with the following security constraints:

```yaml
securityContext:
  runAsNonRoot: true
  allowPrivilegeEscalation: false
  capabilities:
    drop:
      - ALL
```

This approach prevents privilege escalation attacks and follows the principle of least privilege. For example, in a Dockerfile, prefer `USER 1000` over `USER jovyan` to ensure compatibility with security contexts that enforce non-root execution. This practice enhances security in various Kubernetes environments, including those that don't automatically apply these restrictions.


[
  {
    "discussion_id": "1660234226",
    "pr_number": 7622,
    "pr_file": "components/example-notebook-servers/base/Dockerfile",
    "created_at": "2024-06-30T18:56:09+00:00",
    "commented_code": "# common environemnt variables\nENV NB_USER jovyan",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1660234226",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7622,
        "pr_file": "components/example-notebook-servers/base/Dockerfile",
        "discussion_id": "1660234226",
        "commented_code": "@@ -10,6 +10,11 @@ ARG TARGETARCH\n # common environemnt variables\n ENV NB_USER jovyan",
        "comment_created_at": "2024-06-30T18:56:09+00:00",
        "comment_author": "jiridanek",
        "comment_body": "I recently had https://issues.redhat.com/browse/RHOAIENG-72 in my hands, and there the problem was using a symbolic username in the `USER jovyan` statement at the end of the Dockerfile.\r\n\r\nThese images already used the uid even before this PR, so this is good, and therefore \".spec.template.spec.securityContext.runAsNonRoot\" works fine for the images. The runAsNonRoot is something that's normally not set on OpenShifts (where we have SCCs that do the random-uid-0-gid thing), but it's good to be ready for it, and other Kubernetes is more likely to use this.",
        "pr_file_module": null
      },
      {
        "comment_id": "1660306770",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7622,
        "pr_file": "components/example-notebook-servers/base/Dockerfile",
        "discussion_id": "1660234226",
        "commented_code": "@@ -10,6 +10,11 @@ ARG TARGETARCH\n # common environemnt variables\n ENV NB_USER jovyan",
        "comment_created_at": "2024-06-30T20:54:34+00:00",
        "comment_author": "thesuperzapper",
        "comment_body": "@jiridanek To be clear, the issue we are fixing by this PR is mainly about the following `securityContext` configs, which previously the images did not work with:\r\n\r\n```\r\n            allowPrivilegeEscalation: false\r\n            capabilities:\r\n              drop:\r\n                - ALL\r\n```",
        "pr_file_module": null
      }
    ]
  }
]
