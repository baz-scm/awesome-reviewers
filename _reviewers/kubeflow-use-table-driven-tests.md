---
title: Use table-driven tests
description: In Go, prefer table-driven tests over multiple separate test functions.
  Table tests allow for concise testing of multiple scenarios, improve code readability,
  and make it easier to add new test cases.
repository: kubeflow/kubeflow
label: Testing
language: Go
comments_count: 3
repository_stars: 15064
---

In Go, prefer table-driven tests over multiple separate test functions. Table tests allow for concise testing of multiple scenarios, improve code readability, and make it easier to add new test cases.

A table-driven test consists of:
1. A slice of test cases, each containing input and expected output
2. A loop that executes the same test logic for each case
3. Clear error messages that identify which test case failed

Example:
```go
func TestSomething(t *testing.T) {
    tests := []struct {
        name     string
        input    map[string]string
        expected map[string]string
    }{
        {
            name:     "case1",
            input:    map[string]string{"key1": "value1"},
            expected: map[string]string{"key1": "value1", "defaultKey": "defaultValue"},
        },
        {
            name:     "case2",
            input:    map[string]string{},
            expected: map[string]string{"defaultKey": "defaultValue"},
        },
    }
    
    for _, test := range tests {
        t.Run(test.name, func(t *testing.T) {
            result := functionUnderTest(test.input)
            if !reflect.DeepEqual(result, test.expected) {
                t.Errorf("Expected:\n%v\nGot:\n%v", test.expected, result)
            }
        })
    }
}
```

This pattern makes your test suite more maintainable and encourages thorough testing of edge cases by making it trivial to add new scenarios. When reviewing code, ensure new functionality is tested with table-driven tests rather than creating separate test functions for related scenarios.


[
  {
    "discussion_id": "618190706",
    "pr_number": 5761,
    "pr_file": "components/profile-controller/controllers/profile_controller_test.go",
    "created_at": "2021-04-22T08:26:44+00:00",
    "commented_code": "},\n\t}\n\tfor _, test := range tests {\n\t\tupdateNamespaceLabels(test[\"current\"])\n\t\tdefaultKubeflowNamespaceLabels = map[string]string{\n\t\t\t\"katib-metricscollector-injection\":      \"enabled\",\n\t\t\t\"serving.kubeflow.org/inferenceservice\": \"enabled\",\n\t\t\t\"pipelines.kubeflow.org/enabled\":        \"true\",\n\t\t\t\"app.kubernetes.io/part-of\":             \"kubeflow-profile\",\n\t\t}\n\t\tsetNamespaceLabelsFromConfig(test[\"current\"])\n\t\tif !reflect.DeepEqual(test[\"expected\"], test[\"current\"]) {\n\t\t\tt.Errorf(\"Expect:\\n%v; Output:\\n%v\", test[\"current\"], test[\"expected\"])\n\t\t\tt.Errorf(\"Expect:\\n%v; Output:\\n%v\", test[\"expected\"], test[\"current\"])\n\t\t}\n\t}\n}\n\nfunc TestUpdateNamespaceLabels_withLabelRemoval(t *testing.T) {",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "618190706",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5761,
        "pr_file": "components/profile-controller/controllers/profile_controller_test.go",
        "discussion_id": "618190706",
        "commented_code": "@@ -54,9 +54,51 @@ func TestUpdateNamespaceLabels(t *testing.T) {\n \t\t},\n \t}\n \tfor _, test := range tests {\n-\t\tupdateNamespaceLabels(test[\"current\"])\n+\t\tdefaultKubeflowNamespaceLabels = map[string]string{\n+\t\t\t\"katib-metricscollector-injection\":      \"enabled\",\n+\t\t\t\"serving.kubeflow.org/inferenceservice\": \"enabled\",\n+\t\t\t\"pipelines.kubeflow.org/enabled\":        \"true\",\n+\t\t\t\"app.kubernetes.io/part-of\":             \"kubeflow-profile\",\n+\t\t}\n+\t\tsetNamespaceLabelsFromConfig(test[\"current\"])\n \t\tif !reflect.DeepEqual(test[\"expected\"], test[\"current\"]) {\n-\t\t\tt.Errorf(\"Expect:\\n%v; Output:\\n%v\", test[\"current\"], test[\"expected\"])\n+\t\t\tt.Errorf(\"Expect:\\n%v; Output:\\n%v\", test[\"expected\"], test[\"current\"])\n \t\t}\n \t}\n }\n+\n+func TestUpdateNamespaceLabels_withLabelRemoval(t *testing.T) {",
        "comment_created_at": "2021-04-22T08:26:44+00:00",
        "comment_author": "Bobgy",
        "comment_body": "nit: suggest merging this with TestEnforceNamespaceLabelsFromConfig, and allow a test case to specify config yaml.\r\nIn go, we typically prefer table tests than separate test funcs.",
        "pr_file_module": null
      },
      {
        "comment_id": "618735327",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5761,
        "pr_file": "components/profile-controller/controllers/profile_controller_test.go",
        "discussion_id": "618190706",
        "commented_code": "@@ -54,9 +54,51 @@ func TestUpdateNamespaceLabels(t *testing.T) {\n \t\t},\n \t}\n \tfor _, test := range tests {\n-\t\tupdateNamespaceLabels(test[\"current\"])\n+\t\tdefaultKubeflowNamespaceLabels = map[string]string{\n+\t\t\t\"katib-metricscollector-injection\":      \"enabled\",\n+\t\t\t\"serving.kubeflow.org/inferenceservice\": \"enabled\",\n+\t\t\t\"pipelines.kubeflow.org/enabled\":        \"true\",\n+\t\t\t\"app.kubernetes.io/part-of\":             \"kubeflow-profile\",\n+\t\t}\n+\t\tsetNamespaceLabelsFromConfig(test[\"current\"])\n \t\tif !reflect.DeepEqual(test[\"expected\"], test[\"current\"]) {\n-\t\t\tt.Errorf(\"Expect:\\n%v; Output:\\n%v\", test[\"current\"], test[\"expected\"])\n+\t\t\tt.Errorf(\"Expect:\\n%v; Output:\\n%v\", test[\"expected\"], test[\"current\"])\n \t\t}\n \t}\n }\n+\n+func TestUpdateNamespaceLabels_withLabelRemoval(t *testing.T) {",
        "comment_created_at": "2021-04-22T21:00:22+00:00",
        "comment_author": "zijianjoy",
        "comment_body": "Updated to use table tests. ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "956005218",
    "pr_number": 6628,
    "pr_file": "components/notebook-controller/controllers/notebook_controller.go",
    "created_at": "2022-08-26T12:45:06+00:00",
    "commented_code": "return ctrl.Result{RequeueAfter: culler.GetRequeueTime()}, nil\n}\n\nfunc updateNotebookStatus(r *NotebookReconciler, nb *v1beta1.Notebook,",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "956005218",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6628,
        "pr_file": "components/notebook-controller/controllers/notebook_controller.go",
        "discussion_id": "956005218",
        "commented_code": "@@ -324,6 +269,102 @@ func (r *NotebookReconciler) Reconcile(ctx context.Context, req ctrl.Request) (c\n \treturn ctrl.Result{RequeueAfter: culler.GetRequeueTime()}, nil\n }\n \n+func updateNotebookStatus(r *NotebookReconciler, nb *v1beta1.Notebook,",
        "comment_created_at": "2022-08-26T12:45:06+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "Let's change the name of this function to `createNotebookStatus` and update it's signature to:\r\n```golang\r\nfunc createNotebookStatus(r *NotebookReconciler, nb *v1beta1.Notebook,\r\n\tsts *appsv1.StatefulSet, pod *corev1.Pod, req ctrl.Request) (v1beta1.NotebookStatus, error) {\r\n```\r\n\r\nThis means that:\r\n1. We will be passing all necessary objects, statefulset, pod, as arguments\r\n2. The function will be just calculating the status\r\n\r\nThis will also allow us to write some unit tests to ensure we calculate the status as expected.",
        "pr_file_module": null
      },
      {
        "comment_id": "957338776",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6628,
        "pr_file": "components/notebook-controller/controllers/notebook_controller.go",
        "discussion_id": "956005218",
        "commented_code": "@@ -324,6 +269,102 @@ func (r *NotebookReconciler) Reconcile(ctx context.Context, req ctrl.Request) (c\n \treturn ctrl.Result{RequeueAfter: culler.GetRequeueTime()}, nil\n }\n \n+func updateNotebookStatus(r *NotebookReconciler, nb *v1beta1.Notebook,",
        "comment_created_at": "2022-08-29T13:29:31+00:00",
        "comment_author": "apo-ger",
        "comment_body": "Done! I have also added some basic unit tests. Let me know if everything is ok ",
        "pr_file_module": null
      },
      {
        "comment_id": "957500711",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6628,
        "pr_file": "components/notebook-controller/controllers/notebook_controller.go",
        "discussion_id": "956005218",
        "commented_code": "@@ -324,6 +269,102 @@ func (r *NotebookReconciler) Reconcile(ctx context.Context, req ctrl.Request) (c\n \treturn ctrl.Result{RequeueAfter: culler.GetRequeueTime()}, nil\n }\n \n+func updateNotebookStatus(r *NotebookReconciler, nb *v1beta1.Notebook,",
        "comment_created_at": "2022-08-29T15:41:13+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "Nice! Let's also include another unit test for the case where the Notebook's Pod is unschedulable",
        "pr_file_module": null
      },
      {
        "comment_id": "958375886",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6628,
        "pr_file": "components/notebook-controller/controllers/notebook_controller.go",
        "discussion_id": "956005218",
        "commented_code": "@@ -324,6 +269,102 @@ func (r *NotebookReconciler) Reconcile(ctx context.Context, req ctrl.Request) (c\n \treturn ctrl.Result{RequeueAfter: culler.GetRequeueTime()}, nil\n }\n \n+func updateNotebookStatus(r *NotebookReconciler, nb *v1beta1.Notebook,",
        "comment_created_at": "2022-08-30T11:47:27+00:00",
        "comment_author": "apo-ger",
        "comment_body": "Done! ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "518703865",
    "pr_number": 5378,
    "pr_file": "components/notebook-controller/controllers/functional_test.go",
    "created_at": "2020-11-06T11:53:15+00:00",
    "commented_code": "/*\n\nLicensed under the Apache License, Version 2.0 (the \"License\");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n    http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an \"AS IS\" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n*/\n\npackage controllers\n\nimport (\n\t\"context\"\n\t\"time\"\n\n\t. \"github.com/onsi/ginkgo\"\n\t. \"github.com/onsi/gomega\"\n\tappsv1 \"k8s.io/api/apps/v1\"\n\tv1 \"k8s.io/api/core/v1\"\n\tmetav1 \"k8s.io/apimachinery/pkg/apis/meta/v1\"\n\t\"k8s.io/apimachinery/pkg/types\"\n\n\tbeta1 \"github.com/kubeflow/kubeflow/components/notebook-controller/api/v1beta1\"\n)\n\nvar _ = Describe(\"Notebook controller\", func() {\n\n\t// Define utility constants for object names and testing timeouts/durations and intervals.\n\tconst (\n\t\tName      = \"test-notebook\"\n\t\tNamespace = \"default\"\n\t\ttimeout   = time.Second * 10\n\t\tinterval  = time.Millisecond * 250\n\t)\n\n\tContext(\"When validating the notebook controller\", func() {\n\t\tIt(\"Should create replicas\", func() {\n\t\t\tBy(\"By creating a new Notebook\")\n\t\t\tctx := context.Background()\n\t\t\tnotebook := &beta1.Notebook{\n\t\t\t\tObjectMeta: metav1.ObjectMeta{\n\t\t\t\t\tName:      Name,\n\t\t\t\t\tNamespace: Namespace,\n\t\t\t\t},\n\t\t\t\tSpec: beta1.NotebookSpec{\n\t\t\t\t\tTemplate: beta1.NotebookTemplateSpec{\n\t\t\t\t\t\tSpec: v1.PodSpec{Containers: []v1.Container{{\n\t\t\t\t\t\t\tName:  \"busybox\",\n\t\t\t\t\t\t\tImage: \"busybox\",\n\t\t\t\t\t\t}}}},\n\t\t\t\t}}\n\t\t\tExpect(k8sClient.Create(ctx, notebook)).Should(Succeed())\n\n\t\t\tnotebookLookupKey := types.NamespacedName{Name: Name, Namespace: Namespace}\n\t\t\tcreatedNotebook := &beta1.Notebook{}\n\n\t\t\tEventually(func() bool {\n\t\t\t\terr := k8sClient.Get(ctx, notebookLookupKey, createdNotebook)\n\t\t\t\tif err != nil {\n\t\t\t\t\treturn false\n\t\t\t\t}\n\t\t\t\treturn true\n\t\t\t}, timeout, interval).Should(BeTrue())\n\t\t\t/*\n\t\t\t\tChecking for the underlying statefulset\n\t\t\t*/\n\t\t\tBy(\"By checking that the Notebook has statefulset\")\n\t\t\tEventually(func() (bool, error) {\n\t\t\t\tsts := &appsv1.StatefulSet{ObjectMeta: metav1.ObjectMeta{\n\t\t\t\t\tName:      Name,\n\t\t\t\t\tNamespace: Namespace,\n\t\t\t\t}}\n\t\t\t\terr := k8sClient.Get(ctx, notebookLookupKey, sts)\n\t\t\t\tif err != nil {\n\t\t\t\t\treturn false, err\n\t\t\t\t}\n\t\t\t\treturn true, nil\n\t\t\t}, timeout, interval).Should(BeTrue())\n\t\t\t/*\n\t\t\t\tChecking for replica count\n\t\t\t*/\n\t\t\tBy(\"By checking that the Notebook is running with at least 1 replica\")\n\t\t\tEventually(func() bool {\n\t\t\t\treturn notebook.Status.ReadyReplicas > 0\n\t\t\t}, timeout, interval).ShouldNot(Equal(0))",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "518703865",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5378,
        "pr_file": "components/notebook-controller/controllers/functional_test.go",
        "discussion_id": "518703865",
        "commented_code": "@@ -0,0 +1,94 @@\n+/*\n+\n+Licensed under the Apache License, Version 2.0 (the \"License\");\n+you may not use this file except in compliance with the License.\n+You may obtain a copy of the License at\n+\n+    http://www.apache.org/licenses/LICENSE-2.0\n+\n+Unless required by applicable law or agreed to in writing, software\n+distributed under the License is distributed on an \"AS IS\" BASIS,\n+WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n+See the License for the specific language governing permissions and\n+limitations under the License.\n+*/\n+\n+package controllers\n+\n+import (\n+\t\"context\"\n+\t\"time\"\n+\n+\t. \"github.com/onsi/ginkgo\"\n+\t. \"github.com/onsi/gomega\"\n+\tappsv1 \"k8s.io/api/apps/v1\"\n+\tv1 \"k8s.io/api/core/v1\"\n+\tmetav1 \"k8s.io/apimachinery/pkg/apis/meta/v1\"\n+\t\"k8s.io/apimachinery/pkg/types\"\n+\n+\tbeta1 \"github.com/kubeflow/kubeflow/components/notebook-controller/api/v1beta1\"\n+)\n+\n+var _ = Describe(\"Notebook controller\", func() {\n+\n+\t// Define utility constants for object names and testing timeouts/durations and intervals.\n+\tconst (\n+\t\tName      = \"test-notebook\"\n+\t\tNamespace = \"default\"\n+\t\ttimeout   = time.Second * 10\n+\t\tinterval  = time.Millisecond * 250\n+\t)\n+\n+\tContext(\"When validating the notebook controller\", func() {\n+\t\tIt(\"Should create replicas\", func() {\n+\t\t\tBy(\"By creating a new Notebook\")\n+\t\t\tctx := context.Background()\n+\t\t\tnotebook := &beta1.Notebook{\n+\t\t\t\tObjectMeta: metav1.ObjectMeta{\n+\t\t\t\t\tName:      Name,\n+\t\t\t\t\tNamespace: Namespace,\n+\t\t\t\t},\n+\t\t\t\tSpec: beta1.NotebookSpec{\n+\t\t\t\t\tTemplate: beta1.NotebookTemplateSpec{\n+\t\t\t\t\t\tSpec: v1.PodSpec{Containers: []v1.Container{{\n+\t\t\t\t\t\t\tName:  \"busybox\",\n+\t\t\t\t\t\t\tImage: \"busybox\",\n+\t\t\t\t\t\t}}}},\n+\t\t\t\t}}\n+\t\t\tExpect(k8sClient.Create(ctx, notebook)).Should(Succeed())\n+\n+\t\t\tnotebookLookupKey := types.NamespacedName{Name: Name, Namespace: Namespace}\n+\t\t\tcreatedNotebook := &beta1.Notebook{}\n+\n+\t\t\tEventually(func() bool {\n+\t\t\t\terr := k8sClient.Get(ctx, notebookLookupKey, createdNotebook)\n+\t\t\t\tif err != nil {\n+\t\t\t\t\treturn false\n+\t\t\t\t}\n+\t\t\t\treturn true\n+\t\t\t}, timeout, interval).Should(BeTrue())\n+\t\t\t/*\n+\t\t\t\tChecking for the underlying statefulset\n+\t\t\t*/\n+\t\t\tBy(\"By checking that the Notebook has statefulset\")\n+\t\t\tEventually(func() (bool, error) {\n+\t\t\t\tsts := &appsv1.StatefulSet{ObjectMeta: metav1.ObjectMeta{\n+\t\t\t\t\tName:      Name,\n+\t\t\t\t\tNamespace: Namespace,\n+\t\t\t\t}}\n+\t\t\t\terr := k8sClient.Get(ctx, notebookLookupKey, sts)\n+\t\t\t\tif err != nil {\n+\t\t\t\t\treturn false, err\n+\t\t\t\t}\n+\t\t\t\treturn true, nil\n+\t\t\t}, timeout, interval).Should(BeTrue())\n+\t\t\t/*\n+\t\t\t\tChecking for replica count\n+\t\t\t*/\n+\t\t\tBy(\"By checking that the Notebook is running with at least 1 replica\")\n+\t\t\tEventually(func() bool {\n+\t\t\t\treturn notebook.Status.ReadyReplicas > 0\n+\t\t\t}, timeout, interval).ShouldNot(Equal(0))",
        "comment_created_at": "2020-11-06T11:53:15+00:00",
        "comment_author": "yanniszark",
        "comment_body": "Is this correct? You return a bool but then check if it equal to zero (False).\r\nSo in this case, you actually check if `notebook.Status.ReadyReplicas <= 0`.\r\nI attempted to change this to:\r\n\r\n```go\r\n\t\t\tBy(\"By checking that the Notebook is running with at least 1 replica\")\r\n\t\t\tEventually(func() int32 {\r\n\t\t\t\t// Shouldn't we get the statefulset again?\r\n\t\t\t\treturn notebook.Status.ReadyReplicas\r\n\t\t\t}, timeout, interval).ShouldNot(BeZero())\r\n```\r\nbut the test failed.\r\n\r\nWhich leads me to ask, in controller-runtime's test environment, is the statefulset controller running?\r\nIf it is running, what happens to the Pods it creates? I assume that they can't be scheduled, as there is no Node for them to be scheduled to. Can you dig a bit deeper on what happens with Pods in controller-runtime's test env and if they have any suggestions?\r\n\r\nFinally, you wrapped the replica check in an `Eventually` block, but since the block doesn't get the statefulset again, the retries are meaningless.",
        "pr_file_module": null
      },
      {
        "comment_id": "518888927",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5378,
        "pr_file": "components/notebook-controller/controllers/functional_test.go",
        "discussion_id": "518703865",
        "commented_code": "@@ -0,0 +1,94 @@\n+/*\n+\n+Licensed under the Apache License, Version 2.0 (the \"License\");\n+you may not use this file except in compliance with the License.\n+You may obtain a copy of the License at\n+\n+    http://www.apache.org/licenses/LICENSE-2.0\n+\n+Unless required by applicable law or agreed to in writing, software\n+distributed under the License is distributed on an \"AS IS\" BASIS,\n+WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n+See the License for the specific language governing permissions and\n+limitations under the License.\n+*/\n+\n+package controllers\n+\n+import (\n+\t\"context\"\n+\t\"time\"\n+\n+\t. \"github.com/onsi/ginkgo\"\n+\t. \"github.com/onsi/gomega\"\n+\tappsv1 \"k8s.io/api/apps/v1\"\n+\tv1 \"k8s.io/api/core/v1\"\n+\tmetav1 \"k8s.io/apimachinery/pkg/apis/meta/v1\"\n+\t\"k8s.io/apimachinery/pkg/types\"\n+\n+\tbeta1 \"github.com/kubeflow/kubeflow/components/notebook-controller/api/v1beta1\"\n+)\n+\n+var _ = Describe(\"Notebook controller\", func() {\n+\n+\t// Define utility constants for object names and testing timeouts/durations and intervals.\n+\tconst (\n+\t\tName      = \"test-notebook\"\n+\t\tNamespace = \"default\"\n+\t\ttimeout   = time.Second * 10\n+\t\tinterval  = time.Millisecond * 250\n+\t)\n+\n+\tContext(\"When validating the notebook controller\", func() {\n+\t\tIt(\"Should create replicas\", func() {\n+\t\t\tBy(\"By creating a new Notebook\")\n+\t\t\tctx := context.Background()\n+\t\t\tnotebook := &beta1.Notebook{\n+\t\t\t\tObjectMeta: metav1.ObjectMeta{\n+\t\t\t\t\tName:      Name,\n+\t\t\t\t\tNamespace: Namespace,\n+\t\t\t\t},\n+\t\t\t\tSpec: beta1.NotebookSpec{\n+\t\t\t\t\tTemplate: beta1.NotebookTemplateSpec{\n+\t\t\t\t\t\tSpec: v1.PodSpec{Containers: []v1.Container{{\n+\t\t\t\t\t\t\tName:  \"busybox\",\n+\t\t\t\t\t\t\tImage: \"busybox\",\n+\t\t\t\t\t\t}}}},\n+\t\t\t\t}}\n+\t\t\tExpect(k8sClient.Create(ctx, notebook)).Should(Succeed())\n+\n+\t\t\tnotebookLookupKey := types.NamespacedName{Name: Name, Namespace: Namespace}\n+\t\t\tcreatedNotebook := &beta1.Notebook{}\n+\n+\t\t\tEventually(func() bool {\n+\t\t\t\terr := k8sClient.Get(ctx, notebookLookupKey, createdNotebook)\n+\t\t\t\tif err != nil {\n+\t\t\t\t\treturn false\n+\t\t\t\t}\n+\t\t\t\treturn true\n+\t\t\t}, timeout, interval).Should(BeTrue())\n+\t\t\t/*\n+\t\t\t\tChecking for the underlying statefulset\n+\t\t\t*/\n+\t\t\tBy(\"By checking that the Notebook has statefulset\")\n+\t\t\tEventually(func() (bool, error) {\n+\t\t\t\tsts := &appsv1.StatefulSet{ObjectMeta: metav1.ObjectMeta{\n+\t\t\t\t\tName:      Name,\n+\t\t\t\t\tNamespace: Namespace,\n+\t\t\t\t}}\n+\t\t\t\terr := k8sClient.Get(ctx, notebookLookupKey, sts)\n+\t\t\t\tif err != nil {\n+\t\t\t\t\treturn false, err\n+\t\t\t\t}\n+\t\t\t\treturn true, nil\n+\t\t\t}, timeout, interval).Should(BeTrue())\n+\t\t\t/*\n+\t\t\t\tChecking for replica count\n+\t\t\t*/\n+\t\t\tBy(\"By checking that the Notebook is running with at least 1 replica\")\n+\t\t\tEventually(func() bool {\n+\t\t\t\treturn notebook.Status.ReadyReplicas > 0\n+\t\t\t}, timeout, interval).ShouldNot(Equal(0))",
        "comment_created_at": "2020-11-06T17:12:22+00:00",
        "comment_author": "naveensrinivasan",
        "comment_body": "I agree on Pod it creates can't be scheduled without a Node. I will check on that.\r\n\r\nAlso \ud83e\udd26  on the replica check in the `Eventually` block without getting the state refreshed.\r\nIt should be more like this.\r\n\r\n``` go\r\nBy(\"By checking that the Notebook is running with at least 1 replica\")\r\n\t\t\tEventually(func() int32 {\r\n\t\t\t\terr := k8sClient.Get(ctx, notebookLookupKey, createdNotebook)\r\n\t\t\t\tif err != nil {\r\n\t\t\t\t\treturn 0\r\n\t\t\t\t}\r\n\t\t\t\treturn createdNotebook.Status.ReadyReplicas\r\n\t\t\t}, timeout, interval).ShouldNot(BeZero())\r\n```\r\n\r\nIf the controller runtime does not have an option to create `pod` then probably this test would have to be changed. \r\nBut I am not confident about the controller runtime not having that. Let me check and keep you posted.\r\n\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "518945153",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5378,
        "pr_file": "components/notebook-controller/controllers/functional_test.go",
        "discussion_id": "518703865",
        "commented_code": "@@ -0,0 +1,94 @@\n+/*\n+\n+Licensed under the Apache License, Version 2.0 (the \"License\");\n+you may not use this file except in compliance with the License.\n+You may obtain a copy of the License at\n+\n+    http://www.apache.org/licenses/LICENSE-2.0\n+\n+Unless required by applicable law or agreed to in writing, software\n+distributed under the License is distributed on an \"AS IS\" BASIS,\n+WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n+See the License for the specific language governing permissions and\n+limitations under the License.\n+*/\n+\n+package controllers\n+\n+import (\n+\t\"context\"\n+\t\"time\"\n+\n+\t. \"github.com/onsi/ginkgo\"\n+\t. \"github.com/onsi/gomega\"\n+\tappsv1 \"k8s.io/api/apps/v1\"\n+\tv1 \"k8s.io/api/core/v1\"\n+\tmetav1 \"k8s.io/apimachinery/pkg/apis/meta/v1\"\n+\t\"k8s.io/apimachinery/pkg/types\"\n+\n+\tbeta1 \"github.com/kubeflow/kubeflow/components/notebook-controller/api/v1beta1\"\n+)\n+\n+var _ = Describe(\"Notebook controller\", func() {\n+\n+\t// Define utility constants for object names and testing timeouts/durations and intervals.\n+\tconst (\n+\t\tName      = \"test-notebook\"\n+\t\tNamespace = \"default\"\n+\t\ttimeout   = time.Second * 10\n+\t\tinterval  = time.Millisecond * 250\n+\t)\n+\n+\tContext(\"When validating the notebook controller\", func() {\n+\t\tIt(\"Should create replicas\", func() {\n+\t\t\tBy(\"By creating a new Notebook\")\n+\t\t\tctx := context.Background()\n+\t\t\tnotebook := &beta1.Notebook{\n+\t\t\t\tObjectMeta: metav1.ObjectMeta{\n+\t\t\t\t\tName:      Name,\n+\t\t\t\t\tNamespace: Namespace,\n+\t\t\t\t},\n+\t\t\t\tSpec: beta1.NotebookSpec{\n+\t\t\t\t\tTemplate: beta1.NotebookTemplateSpec{\n+\t\t\t\t\t\tSpec: v1.PodSpec{Containers: []v1.Container{{\n+\t\t\t\t\t\t\tName:  \"busybox\",\n+\t\t\t\t\t\t\tImage: \"busybox\",\n+\t\t\t\t\t\t}}}},\n+\t\t\t\t}}\n+\t\t\tExpect(k8sClient.Create(ctx, notebook)).Should(Succeed())\n+\n+\t\t\tnotebookLookupKey := types.NamespacedName{Name: Name, Namespace: Namespace}\n+\t\t\tcreatedNotebook := &beta1.Notebook{}\n+\n+\t\t\tEventually(func() bool {\n+\t\t\t\terr := k8sClient.Get(ctx, notebookLookupKey, createdNotebook)\n+\t\t\t\tif err != nil {\n+\t\t\t\t\treturn false\n+\t\t\t\t}\n+\t\t\t\treturn true\n+\t\t\t}, timeout, interval).Should(BeTrue())\n+\t\t\t/*\n+\t\t\t\tChecking for the underlying statefulset\n+\t\t\t*/\n+\t\t\tBy(\"By checking that the Notebook has statefulset\")\n+\t\t\tEventually(func() (bool, error) {\n+\t\t\t\tsts := &appsv1.StatefulSet{ObjectMeta: metav1.ObjectMeta{\n+\t\t\t\t\tName:      Name,\n+\t\t\t\t\tNamespace: Namespace,\n+\t\t\t\t}}\n+\t\t\t\terr := k8sClient.Get(ctx, notebookLookupKey, sts)\n+\t\t\t\tif err != nil {\n+\t\t\t\t\treturn false, err\n+\t\t\t\t}\n+\t\t\t\treturn true, nil\n+\t\t\t}, timeout, interval).Should(BeTrue())\n+\t\t\t/*\n+\t\t\t\tChecking for replica count\n+\t\t\t*/\n+\t\t\tBy(\"By checking that the Notebook is running with at least 1 replica\")\n+\t\t\tEventually(func() bool {\n+\t\t\t\treturn notebook.Status.ReadyReplicas > 0\n+\t\t\t}, timeout, interval).ShouldNot(Equal(0))",
        "comment_created_at": "2020-11-06T18:59:10+00:00",
        "comment_author": "naveensrinivasan",
        "comment_body": "@yanniszark  I checked on the `envtest` and confirmed that the `statefulset` controller isn't running.  Only the `api server` itself is run by default. So we cannot check the `pod`. So I am refactoring my tests to check for `statefulset`\r\n",
        "pr_file_module": null
      }
    ]
  }
]
