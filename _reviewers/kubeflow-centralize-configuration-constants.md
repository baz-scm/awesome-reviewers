---
title: Centralize configuration constants
description: Store configuration constants, defaults, and environment variable mappings
  in dedicated configuration files rather than duplicating them across the codebase.
  This provides a single source of truth, improves maintainability, and reduces errors
  from inconsistent values.
repository: kubeflow/kubeflow
label: Configurations
language: Python
comments_count: 4
repository_stars: 15064
---

Store configuration constants, defaults, and environment variable mappings in dedicated configuration files rather than duplicating them across the codebase. This provides a single source of truth, improves maintainability, and reduces errors from inconsistent values.

For environment variables with defaults:
```python
# In a central config.py file:
METRICS = bool(os.environ.get("METRICS", False))
BACKEND_MODE = os.environ.get("BACKEND_MODE", BackendMode.PRODUCTION.value)

# In application code:
from config import METRICS, BACKEND_MODE
```

For registry references, version constants, and other configuration mappings:
```python
# In config.py
AWS_REGISTRIES = {
    "jupyter": "public.ecr.aws/j1r0q0g6/jupyter-web-app",
    "volumes": "public.ecr.aws/j1r0q0g6/volumes-web-app",
    # Add more as needed
}

# In application code:
from config import AWS_REGISTRIES
registry = AWS_REGISTRIES["jupyter"]
```

When system-wide defaults are available (like in configmaps), prefer those over hardcoded values to ensure consistency across components.


[
  {
    "discussion_id": "1740935864",
    "pr_number": 7634,
    "pr_file": "components/crud-web-apps/volumes/backend/entrypoint.py",
    "created_at": "2024-09-02T13:33:53+00:00",
    "commented_code": "log = logging.getLogger(__name__)\n\n\ndef get_config(mode):\n    \"\"\"Return a config based on the selected mode.\"\"\"\n    config_classes = {\n        config.BackendMode.DEVELOPMENT.value: config.DevConfig,\n        config.BackendMode.DEVELOPMENT_FULL.value: config.DevConfig,\n        config.BackendMode.PRODUCTION.value: config.ProdConfig,\n        config.BackendMode.PRODUCTION_FULL.value: config.ProdConfig,\n    }\n    cfg_class = config_classes.get(mode)\n    if not cfg_class:\n        raise RuntimeError(\"Backend mode '%s' is not implemented. Choose one\"\n                           \" of %s\" % (mode, list(config_classes.keys())))\n    return cfg_class()\n\n\nAPP_NAME = os.environ.get(\"APP_NAME\", \"Volumes Web App\")\nBACKEND_MODE = os.environ.get(\"BACKEND_MODE\",\n                              config.BackendMode.PRODUCTION.value)\nUI_FLAVOR = os.environ.get(\"UI_FLAVOR\", \"default\")\nPREFIX = os.environ.get(\"APP_PREFIX\", \"/\")\nMETRICS = bool(os.environ.get(\"METRICS\", False))",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1740935864",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7634,
        "pr_file": "components/crud-web-apps/volumes/backend/entrypoint.py",
        "discussion_id": "1740935864",
        "commented_code": "@@ -7,29 +7,16 @@\n log = logging.getLogger(__name__)\n \n \n-def get_config(mode):\n-    \"\"\"Return a config based on the selected mode.\"\"\"\n-    config_classes = {\n-        config.BackendMode.DEVELOPMENT.value: config.DevConfig,\n-        config.BackendMode.DEVELOPMENT_FULL.value: config.DevConfig,\n-        config.BackendMode.PRODUCTION.value: config.ProdConfig,\n-        config.BackendMode.PRODUCTION_FULL.value: config.ProdConfig,\n-    }\n-    cfg_class = config_classes.get(mode)\n-    if not cfg_class:\n-        raise RuntimeError(\"Backend mode '%s' is not implemented. Choose one\"\n-                           \" of %s\" % (mode, list(config_classes.keys())))\n-    return cfg_class()\n-\n-\n APP_NAME = os.environ.get(\"APP_NAME\", \"Volumes Web App\")\n BACKEND_MODE = os.environ.get(\"BACKEND_MODE\",\n                               config.BackendMode.PRODUCTION.value)\n UI_FLAVOR = os.environ.get(\"UI_FLAVOR\", \"default\")\n PREFIX = os.environ.get(\"APP_PREFIX\", \"/\")\n+METRICS = bool(os.environ.get(\"METRICS\", False))",
        "comment_created_at": "2024-09-02T13:33:53+00:00",
        "comment_author": "orfeas-k",
        "comment_body": "Do we need to set a default value both in each specific app and in the config? Maybe we should do it like `backend_mode`\r\n```\r\nBACKEND_MODE = os.environ.get(\"BACKEND_MODE\",\r\n                              config.BackendMode.PRODUCTION.value)\r\n```\r\n\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "1741232798",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7634,
        "pr_file": "components/crud-web-apps/volumes/backend/entrypoint.py",
        "discussion_id": "1740935864",
        "commented_code": "@@ -7,29 +7,16 @@\n log = logging.getLogger(__name__)\n \n \n-def get_config(mode):\n-    \"\"\"Return a config based on the selected mode.\"\"\"\n-    config_classes = {\n-        config.BackendMode.DEVELOPMENT.value: config.DevConfig,\n-        config.BackendMode.DEVELOPMENT_FULL.value: config.DevConfig,\n-        config.BackendMode.PRODUCTION.value: config.ProdConfig,\n-        config.BackendMode.PRODUCTION_FULL.value: config.ProdConfig,\n-    }\n-    cfg_class = config_classes.get(mode)\n-    if not cfg_class:\n-        raise RuntimeError(\"Backend mode '%s' is not implemented. Choose one\"\n-                           \" of %s\" % (mode, list(config_classes.keys())))\n-    return cfg_class()\n-\n-\n APP_NAME = os.environ.get(\"APP_NAME\", \"Volumes Web App\")\n BACKEND_MODE = os.environ.get(\"BACKEND_MODE\",\n                               config.BackendMode.PRODUCTION.value)\n UI_FLAVOR = os.environ.get(\"UI_FLAVOR\", \"default\")\n PREFIX = os.environ.get(\"APP_PREFIX\", \"/\")\n+METRICS = bool(os.environ.get(\"METRICS\", False))",
        "comment_created_at": "2024-09-02T20:20:00+00:00",
        "comment_author": "rgildein",
        "comment_body": "Actually I moved the `self.METRICS = bool(os.environ.get(\"METRICS\", True))` to config __init__, since the logic is for all apps sames (check if env is set to 1, true, ...). WDYT about it?",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "588562507",
    "pr_number": 5663,
    "pr_file": "py/kubeflow/kubeflow/cd/jwa.py",
    "created_at": "2021-03-05T18:30:21+00:00",
    "commented_code": "\"\"\"\"Argo Workflow for building Jupyter web app's OCI image using Kaniko\"\"\"\nimport os\n\nfrom kubeflow.kubeflow import ci\nfrom kubeflow.testing import argo_build_util\n\nTAG = os.getenv(\"PULL_BASE_SHA\", \"kaniko-local-test\")\nAWS_REGISTRY = \"public.ecr.aws/j1r0q0g6/jupyter-web-app\"",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "588562507",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5663,
        "pr_file": "py/kubeflow/kubeflow/cd/jwa.py",
        "discussion_id": "588562507",
        "commented_code": "@@ -0,0 +1,48 @@\n+\"\"\"\"Argo Workflow for building Jupyter web app's OCI image using Kaniko\"\"\"\n+import os\n+\n+from kubeflow.kubeflow import ci\n+from kubeflow.testing import argo_build_util\n+\n+TAG = os.getenv(\"PULL_BASE_SHA\", \"kaniko-local-test\")\n+AWS_REGISTRY = \"public.ecr.aws/j1r0q0g6/jupyter-web-app\"",
        "comment_created_at": "2021-03-05T18:30:21+00:00",
        "comment_author": "PatrickXYS",
        "comment_body": "NIT: since WG-notebooks have multiple ECR registries (7 now, maybe more in the future), I would recommend you maintain a static configmap or mapping in other python files.\r\n\r\nE.g, py/kubeflow/kubeflow/cd/config.py",
        "pr_file_module": null
      },
      {
        "comment_id": "588581750",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5663,
        "pr_file": "py/kubeflow/kubeflow/cd/jwa.py",
        "discussion_id": "588562507",
        "commented_code": "@@ -0,0 +1,48 @@\n+\"\"\"\"Argo Workflow for building Jupyter web app's OCI image using Kaniko\"\"\"\n+import os\n+\n+from kubeflow.kubeflow import ci\n+from kubeflow.testing import argo_build_util\n+\n+TAG = os.getenv(\"PULL_BASE_SHA\", \"kaniko-local-test\")\n+AWS_REGISTRY = \"public.ecr.aws/j1r0q0g6/jupyter-web-app\"",
        "comment_created_at": "2021-03-05T18:51:30+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "That's a good idea, it will help us have all the names organized in one place.\r\nAdding it",
        "pr_file_module": null
      },
      {
        "comment_id": "588603635",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5663,
        "pr_file": "py/kubeflow/kubeflow/cd/jwa.py",
        "discussion_id": "588562507",
        "commented_code": "@@ -0,0 +1,48 @@\n+\"\"\"\"Argo Workflow for building Jupyter web app's OCI image using Kaniko\"\"\"\n+import os\n+\n+from kubeflow.kubeflow import ci\n+from kubeflow.testing import argo_build_util\n+\n+TAG = os.getenv(\"PULL_BASE_SHA\", \"kaniko-local-test\")\n+AWS_REGISTRY = \"public.ecr.aws/j1r0q0g6/jupyter-web-app\"",
        "comment_created_at": "2021-03-05T19:14:27+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "@PatrickXYS I added another commit that introduces this `config.py` file.\r\nPTAL and if you are OK I can resolve this conversation",
        "pr_file_module": null
      },
      {
        "comment_id": "588604805",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5663,
        "pr_file": "py/kubeflow/kubeflow/cd/jwa.py",
        "discussion_id": "588562507",
        "commented_code": "@@ -0,0 +1,48 @@\n+\"\"\"\"Argo Workflow for building Jupyter web app's OCI image using Kaniko\"\"\"\n+import os\n+\n+from kubeflow.kubeflow import ci\n+from kubeflow.testing import argo_build_util\n+\n+TAG = os.getenv(\"PULL_BASE_SHA\", \"kaniko-local-test\")\n+AWS_REGISTRY = \"public.ecr.aws/j1r0q0g6/jupyter-web-app\"",
        "comment_created_at": "2021-03-05T19:15:40+00:00",
        "comment_author": "PatrickXYS",
        "comment_body": "LGTM feel free to resolve",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "570412551",
    "pr_number": 5577,
    "pr_file": "py/kubeflow/kubeflow/ci/workflow_utils.py",
    "created_at": "2021-02-04T17:32:50+00:00",
    "commented_code": "import logging\nimport os\n\nfrom kubeflow.testing import argo_build_util\n\n# The name of the NFS volume claim to use for test files.\nNFS_VOLUME_CLAIM = \"nfs-external\"\n# The name to use for the volume to use to contain test data\nDATA_VOLUME = \"kubeflow-test-volume\"\n\nE2E_DAG_NAME = \"e2e\"\nEXIT_DAG_NAME = \"exit-handler\"\n\n\nLOCAL_TESTING = os.getenv(\"LOCAL_TESTING\", \"False\")\nCREDENTIALS_VOLUME = {\"name\": \"aws-secret\",\n                      \"secret\": {\"secretName\": \"aws-secret\"}}\nCREDENTIALS_MOUNT = {\"mountPath\": \"/root/.aws/\",\n                     \"name\": \"aws-secret\"}\n\nAWS_WORKER_IMAGE = (\"527798164940.dkr.ecr.us-west-2.amazonaws.com/\"\n                    \"aws-kubeflow-ci/test-worker:latest\")\nPUBLIC_WORKER_IMAGE = \"gcr.io/kubeflow-ci/test-worker:latest\"\n\n\nclass ArgoTestBuilder:\n    def __init__(self, name=None, namespace=None, bucket=None,\n                 test_target_name=None,\n                 **kwargs):\n        self.name = name\n        self.namespace = namespace\n        self.bucket = bucket\n        self.template_label = \"argo_test\"\n        self.test_target_name = test_target_name\n        self.mkdir_task_name = \"make-artifacts-dir\"\n\n        # *********************************************************************\n        #\n        # Define directory locations\n        #\n        # *********************************************************************\n\n        # mount_path is the directory where the volume to store the test data\n        # should be mounted.\n        self.mount_path = \"/mnt/\" + \"test-data-volume\"\n        # test_dir is the root directory for all data for a particular test\n        # run.\n        self.test_dir = self.mount_path + \"/\" + self.name\n        # output_dir is the directory to sync to GCS to contain the output for\n        # this job.\n        self.output_dir = self.test_dir + \"/output\"\n\n        self.artifacts_dir = \"%s/artifacts/junit_%s\" % (self.output_dir, name)\n\n        # source directory where all repos should be checked out\n        self.src_root_dir = \"%s/src\" % self.test_dir\n        # The directory containing the kubeflow/kubeflow repo\n        self.src_dir = \"%s/kubeflow/kubeflow\" % self.src_root_dir\n\n        # Root of testing repo.\n        self.testing_src_dir = os.path.join(self.src_root_dir,\n                                            \"kubeflow/testing\")\n\n        # Top level directories for python code\n        self.kubeflow_py = self.src_dir\n\n        # The directory within the kubeflow_testing submodule containing\n        # py scripts to use.\n        self.kubeflow_testing_py = \"%s/kubeflow/testing/py\" % self.src_root_dir\n\n        self.go_path = self.test_dir\n\n    def _build_workflow(self):\n        \"\"\"Create a scaffolding CR for the Argo workflow\"\"\"\n        volumes = [{\n            \"name\": DATA_VOLUME,\n            \"persistentVolumeClaim\": {\n                \"claimName\": NFS_VOLUME_CLAIM\n            },\n        }]\n        if LOCAL_TESTING == \"False\":\n            volumes.append(CREDENTIALS_VOLUME)\n\n        workflow = {\n            \"apiVersion\": \"argoproj.io/v1alpha1\",\n            \"kind\": \"Workflow\",\n            \"metadata\": {\n                \"name\": self.name,\n                \"namespace\": self.namespace,\n                \"labels\": argo_build_util.add_dicts([\n                    {\n                        \"workflow\": self.name,\n                        \"workflow_template\": self.template_label,\n                    },\n                    argo_build_util.get_prow_labels()\n                ]),\n            },\n            \"spec\": {\n                \"entrypoint\": E2E_DAG_NAME,\n                # Have argo garbage collect old workflows otherwise we overload\n                # the API server.\n                \"ttlSecondsAfterFinished\": 7 * 24 * 60 * 60,",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "570412551",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5577,
        "pr_file": "py/kubeflow/kubeflow/ci/workflow_utils.py",
        "discussion_id": "570412551",
        "commented_code": "@@ -0,0 +1,249 @@\n+import logging\n+import os\n+\n+from kubeflow.testing import argo_build_util\n+\n+# The name of the NFS volume claim to use for test files.\n+NFS_VOLUME_CLAIM = \"nfs-external\"\n+# The name to use for the volume to use to contain test data\n+DATA_VOLUME = \"kubeflow-test-volume\"\n+\n+E2E_DAG_NAME = \"e2e\"\n+EXIT_DAG_NAME = \"exit-handler\"\n+\n+\n+LOCAL_TESTING = os.getenv(\"LOCAL_TESTING\", \"False\")\n+CREDENTIALS_VOLUME = {\"name\": \"aws-secret\",\n+                      \"secret\": {\"secretName\": \"aws-secret\"}}\n+CREDENTIALS_MOUNT = {\"mountPath\": \"/root/.aws/\",\n+                     \"name\": \"aws-secret\"}\n+\n+AWS_WORKER_IMAGE = (\"527798164940.dkr.ecr.us-west-2.amazonaws.com/\"\n+                    \"aws-kubeflow-ci/test-worker:latest\")\n+PUBLIC_WORKER_IMAGE = \"gcr.io/kubeflow-ci/test-worker:latest\"\n+\n+\n+class ArgoTestBuilder:\n+    def __init__(self, name=None, namespace=None, bucket=None,\n+                 test_target_name=None,\n+                 **kwargs):\n+        self.name = name\n+        self.namespace = namespace\n+        self.bucket = bucket\n+        self.template_label = \"argo_test\"\n+        self.test_target_name = test_target_name\n+        self.mkdir_task_name = \"make-artifacts-dir\"\n+\n+        # *********************************************************************\n+        #\n+        # Define directory locations\n+        #\n+        # *********************************************************************\n+\n+        # mount_path is the directory where the volume to store the test data\n+        # should be mounted.\n+        self.mount_path = \"/mnt/\" + \"test-data-volume\"\n+        # test_dir is the root directory for all data for a particular test\n+        # run.\n+        self.test_dir = self.mount_path + \"/\" + self.name\n+        # output_dir is the directory to sync to GCS to contain the output for\n+        # this job.\n+        self.output_dir = self.test_dir + \"/output\"\n+\n+        self.artifacts_dir = \"%s/artifacts/junit_%s\" % (self.output_dir, name)\n+\n+        # source directory where all repos should be checked out\n+        self.src_root_dir = \"%s/src\" % self.test_dir\n+        # The directory containing the kubeflow/kubeflow repo\n+        self.src_dir = \"%s/kubeflow/kubeflow\" % self.src_root_dir\n+\n+        # Root of testing repo.\n+        self.testing_src_dir = os.path.join(self.src_root_dir,\n+                                            \"kubeflow/testing\")\n+\n+        # Top level directories for python code\n+        self.kubeflow_py = self.src_dir\n+\n+        # The directory within the kubeflow_testing submodule containing\n+        # py scripts to use.\n+        self.kubeflow_testing_py = \"%s/kubeflow/testing/py\" % self.src_root_dir\n+\n+        self.go_path = self.test_dir\n+\n+    def _build_workflow(self):\n+        \"\"\"Create a scaffolding CR for the Argo workflow\"\"\"\n+        volumes = [{\n+            \"name\": DATA_VOLUME,\n+            \"persistentVolumeClaim\": {\n+                \"claimName\": NFS_VOLUME_CLAIM\n+            },\n+        }]\n+        if LOCAL_TESTING == \"False\":\n+            volumes.append(CREDENTIALS_VOLUME)\n+\n+        workflow = {\n+            \"apiVersion\": \"argoproj.io/v1alpha1\",\n+            \"kind\": \"Workflow\",\n+            \"metadata\": {\n+                \"name\": self.name,\n+                \"namespace\": self.namespace,\n+                \"labels\": argo_build_util.add_dicts([\n+                    {\n+                        \"workflow\": self.name,\n+                        \"workflow_template\": self.template_label,\n+                    },\n+                    argo_build_util.get_prow_labels()\n+                ]),\n+            },\n+            \"spec\": {\n+                \"entrypoint\": E2E_DAG_NAME,\n+                # Have argo garbage collect old workflows otherwise we overload\n+                # the API server.\n+                \"ttlSecondsAfterFinished\": 7 * 24 * 60 * 60,",
        "comment_created_at": "2021-02-04T17:32:50+00:00",
        "comment_author": "PatrickXYS",
        "comment_body": "In new argo cluster, we installed v2.12.3 argo workflow, this parameter has been deprecated. \r\n\r\nhttps://github.com/argoproj/argo/blob/master/examples/gc-ttl.yaml\r\n\r\nYou can instead use ttlStrategy",
        "pr_file_module": null
      },
      {
        "comment_id": "570425003",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5577,
        "pr_file": "py/kubeflow/kubeflow/ci/workflow_utils.py",
        "discussion_id": "570412551",
        "commented_code": "@@ -0,0 +1,249 @@\n+import logging\n+import os\n+\n+from kubeflow.testing import argo_build_util\n+\n+# The name of the NFS volume claim to use for test files.\n+NFS_VOLUME_CLAIM = \"nfs-external\"\n+# The name to use for the volume to use to contain test data\n+DATA_VOLUME = \"kubeflow-test-volume\"\n+\n+E2E_DAG_NAME = \"e2e\"\n+EXIT_DAG_NAME = \"exit-handler\"\n+\n+\n+LOCAL_TESTING = os.getenv(\"LOCAL_TESTING\", \"False\")\n+CREDENTIALS_VOLUME = {\"name\": \"aws-secret\",\n+                      \"secret\": {\"secretName\": \"aws-secret\"}}\n+CREDENTIALS_MOUNT = {\"mountPath\": \"/root/.aws/\",\n+                     \"name\": \"aws-secret\"}\n+\n+AWS_WORKER_IMAGE = (\"527798164940.dkr.ecr.us-west-2.amazonaws.com/\"\n+                    \"aws-kubeflow-ci/test-worker:latest\")\n+PUBLIC_WORKER_IMAGE = \"gcr.io/kubeflow-ci/test-worker:latest\"\n+\n+\n+class ArgoTestBuilder:\n+    def __init__(self, name=None, namespace=None, bucket=None,\n+                 test_target_name=None,\n+                 **kwargs):\n+        self.name = name\n+        self.namespace = namespace\n+        self.bucket = bucket\n+        self.template_label = \"argo_test\"\n+        self.test_target_name = test_target_name\n+        self.mkdir_task_name = \"make-artifacts-dir\"\n+\n+        # *********************************************************************\n+        #\n+        # Define directory locations\n+        #\n+        # *********************************************************************\n+\n+        # mount_path is the directory where the volume to store the test data\n+        # should be mounted.\n+        self.mount_path = \"/mnt/\" + \"test-data-volume\"\n+        # test_dir is the root directory for all data for a particular test\n+        # run.\n+        self.test_dir = self.mount_path + \"/\" + self.name\n+        # output_dir is the directory to sync to GCS to contain the output for\n+        # this job.\n+        self.output_dir = self.test_dir + \"/output\"\n+\n+        self.artifacts_dir = \"%s/artifacts/junit_%s\" % (self.output_dir, name)\n+\n+        # source directory where all repos should be checked out\n+        self.src_root_dir = \"%s/src\" % self.test_dir\n+        # The directory containing the kubeflow/kubeflow repo\n+        self.src_dir = \"%s/kubeflow/kubeflow\" % self.src_root_dir\n+\n+        # Root of testing repo.\n+        self.testing_src_dir = os.path.join(self.src_root_dir,\n+                                            \"kubeflow/testing\")\n+\n+        # Top level directories for python code\n+        self.kubeflow_py = self.src_dir\n+\n+        # The directory within the kubeflow_testing submodule containing\n+        # py scripts to use.\n+        self.kubeflow_testing_py = \"%s/kubeflow/testing/py\" % self.src_root_dir\n+\n+        self.go_path = self.test_dir\n+\n+    def _build_workflow(self):\n+        \"\"\"Create a scaffolding CR for the Argo workflow\"\"\"\n+        volumes = [{\n+            \"name\": DATA_VOLUME,\n+            \"persistentVolumeClaim\": {\n+                \"claimName\": NFS_VOLUME_CLAIM\n+            },\n+        }]\n+        if LOCAL_TESTING == \"False\":\n+            volumes.append(CREDENTIALS_VOLUME)\n+\n+        workflow = {\n+            \"apiVersion\": \"argoproj.io/v1alpha1\",\n+            \"kind\": \"Workflow\",\n+            \"metadata\": {\n+                \"name\": self.name,\n+                \"namespace\": self.namespace,\n+                \"labels\": argo_build_util.add_dicts([\n+                    {\n+                        \"workflow\": self.name,\n+                        \"workflow_template\": self.template_label,\n+                    },\n+                    argo_build_util.get_prow_labels()\n+                ]),\n+            },\n+            \"spec\": {\n+                \"entrypoint\": E2E_DAG_NAME,\n+                # Have argo garbage collect old workflows otherwise we overload\n+                # the API server.\n+                \"ttlSecondsAfterFinished\": 7 * 24 * 60 * 60,",
        "comment_created_at": "2021-02-04T17:50:25+00:00",
        "comment_author": "PatrickXYS",
        "comment_body": "Or make it simpler, you don't need to set it up, we have already configured default workflow spec \r\n\r\n```\r\nconfigmap -o yaml\r\napiVersion: v1\r\ndata:\r\n  workflowDefaults: |\r\n    metadata:\r\n      annotations:\r\n        argo: workflows\r\n    spec:\r\n      ttlStrategy:\r\n        secondsAfterSuccess: 604800\r\n        secondsAfterCompletion: 604800\r\n        secondsAfterFailure: 604800\r\n      activeDeadlineSeconds: 86400\r\n...\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "570511192",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5577,
        "pr_file": "py/kubeflow/kubeflow/ci/workflow_utils.py",
        "discussion_id": "570412551",
        "commented_code": "@@ -0,0 +1,249 @@\n+import logging\n+import os\n+\n+from kubeflow.testing import argo_build_util\n+\n+# The name of the NFS volume claim to use for test files.\n+NFS_VOLUME_CLAIM = \"nfs-external\"\n+# The name to use for the volume to use to contain test data\n+DATA_VOLUME = \"kubeflow-test-volume\"\n+\n+E2E_DAG_NAME = \"e2e\"\n+EXIT_DAG_NAME = \"exit-handler\"\n+\n+\n+LOCAL_TESTING = os.getenv(\"LOCAL_TESTING\", \"False\")\n+CREDENTIALS_VOLUME = {\"name\": \"aws-secret\",\n+                      \"secret\": {\"secretName\": \"aws-secret\"}}\n+CREDENTIALS_MOUNT = {\"mountPath\": \"/root/.aws/\",\n+                     \"name\": \"aws-secret\"}\n+\n+AWS_WORKER_IMAGE = (\"527798164940.dkr.ecr.us-west-2.amazonaws.com/\"\n+                    \"aws-kubeflow-ci/test-worker:latest\")\n+PUBLIC_WORKER_IMAGE = \"gcr.io/kubeflow-ci/test-worker:latest\"\n+\n+\n+class ArgoTestBuilder:\n+    def __init__(self, name=None, namespace=None, bucket=None,\n+                 test_target_name=None,\n+                 **kwargs):\n+        self.name = name\n+        self.namespace = namespace\n+        self.bucket = bucket\n+        self.template_label = \"argo_test\"\n+        self.test_target_name = test_target_name\n+        self.mkdir_task_name = \"make-artifacts-dir\"\n+\n+        # *********************************************************************\n+        #\n+        # Define directory locations\n+        #\n+        # *********************************************************************\n+\n+        # mount_path is the directory where the volume to store the test data\n+        # should be mounted.\n+        self.mount_path = \"/mnt/\" + \"test-data-volume\"\n+        # test_dir is the root directory for all data for a particular test\n+        # run.\n+        self.test_dir = self.mount_path + \"/\" + self.name\n+        # output_dir is the directory to sync to GCS to contain the output for\n+        # this job.\n+        self.output_dir = self.test_dir + \"/output\"\n+\n+        self.artifacts_dir = \"%s/artifacts/junit_%s\" % (self.output_dir, name)\n+\n+        # source directory where all repos should be checked out\n+        self.src_root_dir = \"%s/src\" % self.test_dir\n+        # The directory containing the kubeflow/kubeflow repo\n+        self.src_dir = \"%s/kubeflow/kubeflow\" % self.src_root_dir\n+\n+        # Root of testing repo.\n+        self.testing_src_dir = os.path.join(self.src_root_dir,\n+                                            \"kubeflow/testing\")\n+\n+        # Top level directories for python code\n+        self.kubeflow_py = self.src_dir\n+\n+        # The directory within the kubeflow_testing submodule containing\n+        # py scripts to use.\n+        self.kubeflow_testing_py = \"%s/kubeflow/testing/py\" % self.src_root_dir\n+\n+        self.go_path = self.test_dir\n+\n+    def _build_workflow(self):\n+        \"\"\"Create a scaffolding CR for the Argo workflow\"\"\"\n+        volumes = [{\n+            \"name\": DATA_VOLUME,\n+            \"persistentVolumeClaim\": {\n+                \"claimName\": NFS_VOLUME_CLAIM\n+            },\n+        }]\n+        if LOCAL_TESTING == \"False\":\n+            volumes.append(CREDENTIALS_VOLUME)\n+\n+        workflow = {\n+            \"apiVersion\": \"argoproj.io/v1alpha1\",\n+            \"kind\": \"Workflow\",\n+            \"metadata\": {\n+                \"name\": self.name,\n+                \"namespace\": self.namespace,\n+                \"labels\": argo_build_util.add_dicts([\n+                    {\n+                        \"workflow\": self.name,\n+                        \"workflow_template\": self.template_label,\n+                    },\n+                    argo_build_util.get_prow_labels()\n+                ]),\n+            },\n+            \"spec\": {\n+                \"entrypoint\": E2E_DAG_NAME,\n+                # Have argo garbage collect old workflows otherwise we overload\n+                # the API server.\n+                \"ttlSecondsAfterFinished\": 7 * 24 * 60 * 60,",
        "comment_created_at": "2021-02-04T20:08:03+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "OK, I'll just omit this field entirely. There no issue by completely omitting the field and the configmap's value will be used right?",
        "pr_file_module": null
      },
      {
        "comment_id": "570516493",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5577,
        "pr_file": "py/kubeflow/kubeflow/ci/workflow_utils.py",
        "discussion_id": "570412551",
        "commented_code": "@@ -0,0 +1,249 @@\n+import logging\n+import os\n+\n+from kubeflow.testing import argo_build_util\n+\n+# The name of the NFS volume claim to use for test files.\n+NFS_VOLUME_CLAIM = \"nfs-external\"\n+# The name to use for the volume to use to contain test data\n+DATA_VOLUME = \"kubeflow-test-volume\"\n+\n+E2E_DAG_NAME = \"e2e\"\n+EXIT_DAG_NAME = \"exit-handler\"\n+\n+\n+LOCAL_TESTING = os.getenv(\"LOCAL_TESTING\", \"False\")\n+CREDENTIALS_VOLUME = {\"name\": \"aws-secret\",\n+                      \"secret\": {\"secretName\": \"aws-secret\"}}\n+CREDENTIALS_MOUNT = {\"mountPath\": \"/root/.aws/\",\n+                     \"name\": \"aws-secret\"}\n+\n+AWS_WORKER_IMAGE = (\"527798164940.dkr.ecr.us-west-2.amazonaws.com/\"\n+                    \"aws-kubeflow-ci/test-worker:latest\")\n+PUBLIC_WORKER_IMAGE = \"gcr.io/kubeflow-ci/test-worker:latest\"\n+\n+\n+class ArgoTestBuilder:\n+    def __init__(self, name=None, namespace=None, bucket=None,\n+                 test_target_name=None,\n+                 **kwargs):\n+        self.name = name\n+        self.namespace = namespace\n+        self.bucket = bucket\n+        self.template_label = \"argo_test\"\n+        self.test_target_name = test_target_name\n+        self.mkdir_task_name = \"make-artifacts-dir\"\n+\n+        # *********************************************************************\n+        #\n+        # Define directory locations\n+        #\n+        # *********************************************************************\n+\n+        # mount_path is the directory where the volume to store the test data\n+        # should be mounted.\n+        self.mount_path = \"/mnt/\" + \"test-data-volume\"\n+        # test_dir is the root directory for all data for a particular test\n+        # run.\n+        self.test_dir = self.mount_path + \"/\" + self.name\n+        # output_dir is the directory to sync to GCS to contain the output for\n+        # this job.\n+        self.output_dir = self.test_dir + \"/output\"\n+\n+        self.artifacts_dir = \"%s/artifacts/junit_%s\" % (self.output_dir, name)\n+\n+        # source directory where all repos should be checked out\n+        self.src_root_dir = \"%s/src\" % self.test_dir\n+        # The directory containing the kubeflow/kubeflow repo\n+        self.src_dir = \"%s/kubeflow/kubeflow\" % self.src_root_dir\n+\n+        # Root of testing repo.\n+        self.testing_src_dir = os.path.join(self.src_root_dir,\n+                                            \"kubeflow/testing\")\n+\n+        # Top level directories for python code\n+        self.kubeflow_py = self.src_dir\n+\n+        # The directory within the kubeflow_testing submodule containing\n+        # py scripts to use.\n+        self.kubeflow_testing_py = \"%s/kubeflow/testing/py\" % self.src_root_dir\n+\n+        self.go_path = self.test_dir\n+\n+    def _build_workflow(self):\n+        \"\"\"Create a scaffolding CR for the Argo workflow\"\"\"\n+        volumes = [{\n+            \"name\": DATA_VOLUME,\n+            \"persistentVolumeClaim\": {\n+                \"claimName\": NFS_VOLUME_CLAIM\n+            },\n+        }]\n+        if LOCAL_TESTING == \"False\":\n+            volumes.append(CREDENTIALS_VOLUME)\n+\n+        workflow = {\n+            \"apiVersion\": \"argoproj.io/v1alpha1\",\n+            \"kind\": \"Workflow\",\n+            \"metadata\": {\n+                \"name\": self.name,\n+                \"namespace\": self.namespace,\n+                \"labels\": argo_build_util.add_dicts([\n+                    {\n+                        \"workflow\": self.name,\n+                        \"workflow_template\": self.template_label,\n+                    },\n+                    argo_build_util.get_prow_labels()\n+                ]),\n+            },\n+            \"spec\": {\n+                \"entrypoint\": E2E_DAG_NAME,\n+                # Have argo garbage collect old workflows otherwise we overload\n+                # the API server.\n+                \"ttlSecondsAfterFinished\": 7 * 24 * 60 * 60,",
        "comment_created_at": "2021-02-04T20:17:21+00:00",
        "comment_author": "PatrickXYS",
        "comment_body": "Yeah default workflow should handle it.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1732661929",
    "pr_number": 7634,
    "pr_file": "components/crud-web-apps/common/backend/setup.py",
    "created_at": "2024-08-27T11:26:07+00:00",
    "commented_code": "\"Werkzeug >= 0.16.0\",\n    \"Flask-Cors >= 3.0.8\",\n    \"gevent\",\n    \"prometheus-flask-exporter >= 0.23.1\",\n    \"importlib-metadata >= 1.0;python_version<'3.8'\",\n]",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1732661929",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7634,
        "pr_file": "components/crud-web-apps/common/backend/setup.py",
        "discussion_id": "1732661929",
        "commented_code": "@@ -9,6 +9,8 @@\n     \"Werkzeug >= 0.16.0\",\n     \"Flask-Cors >= 3.0.8\",\n     \"gevent\",\n+    \"prometheus-flask-exporter >= 0.23.1\",\n+    \"importlib-metadata >= 1.0;python_version<'3.8'\",\n ]",
        "comment_created_at": "2024-08-27T11:26:07+00:00",
        "comment_author": "orfeas-k",
        "comment_body": "Why do we need to set `python_version` here?",
        "pr_file_module": null
      },
      {
        "comment_id": "1734095817",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7634,
        "pr_file": "components/crud-web-apps/common/backend/setup.py",
        "discussion_id": "1732661929",
        "commented_code": "@@ -9,6 +9,8 @@\n     \"Werkzeug >= 0.16.0\",\n     \"Flask-Cors >= 3.0.8\",\n     \"gevent\",\n+    \"prometheus-flask-exporter >= 0.23.1\",\n+    \"importlib-metadata >= 1.0;python_version<'3.8'\",\n ]",
        "comment_created_at": "2024-08-28T06:54:41+00:00",
        "comment_author": "rgildein",
        "comment_body": "From python 3.8 the `importlib.metadata` is build in package. You can see it [here](https://docs.python.org/3.8/library/importlib.metadata.html).",
        "pr_file_module": null
      }
    ]
  }
]
