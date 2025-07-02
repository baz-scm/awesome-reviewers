---
title: Contextualize and classify errors
description: Always provide meaningful context when handling errors, and classify
  them appropriately based on their source. This improves debugging, helps users understand
  issues, and creates a consistent approach to error handling across the codebase.
repository: kubeflow/kubeflow
label: Error Handling
language: Go
comments_count: 4
repository_stars: 15064
---

Always provide meaningful context when handling errors, and classify them appropriately based on their source. This improves debugging, helps users understand issues, and creates a consistent approach to error handling across the codebase.

Follow these error handling principles:

1. **Use early returns with clear error checks**:
```go
if err != nil {
    // Log error and/or return response
    return nil, fmt.Errorf("failed to process request: %v", err)
}
// Handle the success case
```

2. **Provide context in error messages**:
```go
// Instead of just returning or logging the raw error
if _, err := w.Write([]byte(err.Error())); err != nil {
    log.Error(err) // Poor context

    // Better approach with context
    log.Error(fmt.Errorf("failed to write error response: %v", err))
}
```

3. **Distinguish between error variables in nested scopes**:
```go
err := json.NewDecoder(r.Body).Decode(&profile)
if err != nil {
    // Handle first error
    if writeErr := json.NewEncoder(w).Encode(err); writeErr != nil {
        log.Error(fmt.Errorf("decode failed: %v, response write failed: %v", err, writeErr))
    }
    return
}
```

4. **Classify errors properly**:
```go
// For user input errors
return &kfapis.KfError{
    Code:    int(kfapis.INVALID_ARGUMENT),
    Message: fmt.Sprintf("Project not specified: %v", err),
}

// For system/internal errors
return &kfapis.KfError{
    Code:    int(kfapis.INTERNAL_ERROR),
    Message: fmt.Sprintf("Failed to create application: %v", err),
}
```

5. **Use consistent error types** throughout your codebase, and consider creating helper functions to reduce boilerplate:
```go
func NewInvalidArgumentError(err error, msg string) *kfapis.KfError {
    return &kfapis.KfError{
        Code:    int(kfapis.INVALID_ARGUMENT),
        Message: fmt.Sprintf("%s: %v", msg, err),
    }
}
```


[
  {
    "discussion_id": "369260124",
    "pr_number": 4674,
    "pr_file": "components/access-management/kfam/api_default.go",
    "created_at": "2020-01-21T21:46:33+00:00",
    "commented_code": "if c.isOwnerOrAdmin(useremail, binding.ReferredNamespace) {\n\t\terr := c.bindingClient.Create(&binding, c.userIdHeader, c.userIdPrefix)\n\t\tif err == nil {\n\t\t\tIncRequestCounter(\"\", useremail, action, r.URL.Path)\n\t\t\tw.WriteHeader(http.StatusOK)\n\t\t} else {\n\t\t\tIncRequestErrorCounter(err.Error(), useremail, action, r.URL.Path,\n\t\t\t\tSEVERITY_MAJOR)\n\t\t\tw.WriteHeader(http.StatusForbidden)\n\t\t\tw.Write([]byte(err.Error()))\n\t\t\tif _, err := w.Write([]byte(err.Error())); err != nil {\n\t\t\t\tlog.Error(err)\n\t\t\t}\n\t\t}\n\t} else {\n\t\tIncRequestErrorCounter(\"forbidden\", useremail, action, r.URL.Path,\n\t\t\tSEVERITY_MINOR)\n\t\tw.WriteHeader(http.StatusForbidden)\n\t}\n}\n\nfunc (c *KfamV1Alpha1Client) CreateProfile(w http.ResponseWriter, r *http.Request) {\n\tw.Header().Set(\"Content-Type\", \"application/json; charset=UTF-8\")\n\tconst action = \"create\"\n\tvar profile profilev1beta1.Profile\n\tif err := json.NewDecoder(r.Body).Decode(&profile); err != nil {\n\t\tjson.NewEncoder(w).Encode(err)\n\t\tIncRequestErrorCounter(\"decode error\", \"\", action, r.URL.Path,\n\t\t\tSEVERITY_MAJOR)\n\t\tif err := json.NewEncoder(w).Encode(err); err != nil {\n\t\t\tlog.Error(err)\n\t\t}\n\t\tw.WriteHeader(http.StatusForbidden)\n\t\treturn\n\t}\n\t_, err := c.profileClient.Create(&profile)\n\tif err == nil {",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "369260124",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 4674,
        "pr_file": "components/access-management/kfam/api_default.go",
        "discussion_id": "369260124",
        "commented_code": "@@ -102,38 +108,60 @@ func (c *KfamV1Alpha1Client) CreateBinding(w http.ResponseWriter, r *http.Reques\n \tif c.isOwnerOrAdmin(useremail, binding.ReferredNamespace) {\n \t\terr := c.bindingClient.Create(&binding, c.userIdHeader, c.userIdPrefix)\n \t\tif err == nil {\n+\t\t\tIncRequestCounter(\"\", useremail, action, r.URL.Path)\n \t\t\tw.WriteHeader(http.StatusOK)\n \t\t} else {\n+\t\t\tIncRequestErrorCounter(err.Error(), useremail, action, r.URL.Path,\n+\t\t\t\tSEVERITY_MAJOR)\n \t\t\tw.WriteHeader(http.StatusForbidden)\n-\t\t\tw.Write([]byte(err.Error()))\n+\t\t\tif _, err := w.Write([]byte(err.Error())); err != nil {\n+\t\t\t\tlog.Error(err)\n+\t\t\t}\n \t\t}\n \t} else {\n+\t\tIncRequestErrorCounter(\"forbidden\", useremail, action, r.URL.Path,\n+\t\t\tSEVERITY_MINOR)\n \t\tw.WriteHeader(http.StatusForbidden)\n \t}\n }\n \n func (c *KfamV1Alpha1Client) CreateProfile(w http.ResponseWriter, r *http.Request) {\n \tw.Header().Set(\"Content-Type\", \"application/json; charset=UTF-8\")\n+\tconst action = \"create\"\n \tvar profile profilev1beta1.Profile\n \tif err := json.NewDecoder(r.Body).Decode(&profile); err != nil {\n-\t\tjson.NewEncoder(w).Encode(err)\n+\t\tIncRequestErrorCounter(\"decode error\", \"\", action, r.URL.Path,\n+\t\t\tSEVERITY_MAJOR)\n+\t\tif err := json.NewEncoder(w).Encode(err); err != nil {\n+\t\t\tlog.Error(err)\n+\t\t}\n \t\tw.WriteHeader(http.StatusForbidden)\n \t\treturn\n \t}\n \t_, err := c.profileClient.Create(&profile)\n \tif err == nil {",
        "comment_created_at": "2020-01-21T21:46:33+00:00",
        "comment_author": "zhenghuiwang",
        "comment_body": "This if-else now becomes more complex code. I think it is time to consider following the Go error handling pattern to increase readability:\r\n\r\n```\r\nif err != nil {\r\n  // log error and return response.\r\n return\r\n}\r\n// handle the err = nil case\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "369265640",
    "pr_number": 4674,
    "pr_file": "components/access-management/kfam/api_default.go",
    "created_at": "2020-01-21T21:58:53+00:00",
    "commented_code": "if c.isOwnerOrAdmin(useremail, binding.ReferredNamespace) {\n\t\terr := c.bindingClient.Create(&binding, c.userIdHeader, c.userIdPrefix)\n\t\tif err == nil {\n\t\t\tIncRequestCounter(\"\", useremail, action, r.URL.Path)\n\t\t\tw.WriteHeader(http.StatusOK)\n\t\t} else {\n\t\t\tIncRequestErrorCounter(err.Error(), useremail, action, r.URL.Path,\n\t\t\t\tSEVERITY_MAJOR)\n\t\t\tw.WriteHeader(http.StatusForbidden)\n\t\t\tw.Write([]byte(err.Error()))\n\t\t\tif _, err := w.Write([]byte(err.Error())); err != nil {\n\t\t\t\tlog.Error(err)\n\t\t\t}\n\t\t}\n\t} else {\n\t\tIncRequestErrorCounter(\"forbidden\", useremail, action, r.URL.Path,\n\t\t\tSEVERITY_MINOR)\n\t\tw.WriteHeader(http.StatusForbidden)\n\t}\n}\n\nfunc (c *KfamV1Alpha1Client) CreateProfile(w http.ResponseWriter, r *http.Request) {\n\tw.Header().Set(\"Content-Type\", \"application/json; charset=UTF-8\")\n\tconst action = \"create\"\n\tvar profile profilev1beta1.Profile\n\tif err := json.NewDecoder(r.Body).Decode(&profile); err != nil {\n\t\tjson.NewEncoder(w).Encode(err)\n\t\tIncRequestErrorCounter(\"decode error\", \"\", action, r.URL.Path,\n\t\t\tSEVERITY_MAJOR)\n\t\tif err := json.NewEncoder(w).Encode(err); err != nil {\n\t\t\tlog.Error(err)\n\t\t}\n\t\tw.WriteHeader(http.StatusForbidden)\n\t\treturn\n\t}\n\t_, err := c.profileClient.Create(&profile)\n\tif err == nil {\n\t\tIncRequestCounter(\"\", \"\", action, r.URL.Path)\n\t\tw.WriteHeader(http.StatusOK)\n\t} else {\n\t\tIncRequestErrorCounter(err.Error(), \"\", action, r.URL.Path,\n\t\t\tSEVERITY_MAJOR)\n\t\tw.WriteHeader(http.StatusForbidden)\n\t\tw.Write([]byte(err.Error()))\n\t\tif _, err := w.Write([]byte(err.Error())); err != nil {\n\t\t\tlog.Error(err)",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "369265640",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 4674,
        "pr_file": "components/access-management/kfam/api_default.go",
        "discussion_id": "369265640",
        "commented_code": "@@ -102,38 +108,60 @@ func (c *KfamV1Alpha1Client) CreateBinding(w http.ResponseWriter, r *http.Reques\n \tif c.isOwnerOrAdmin(useremail, binding.ReferredNamespace) {\n \t\terr := c.bindingClient.Create(&binding, c.userIdHeader, c.userIdPrefix)\n \t\tif err == nil {\n+\t\t\tIncRequestCounter(\"\", useremail, action, r.URL.Path)\n \t\t\tw.WriteHeader(http.StatusOK)\n \t\t} else {\n+\t\t\tIncRequestErrorCounter(err.Error(), useremail, action, r.URL.Path,\n+\t\t\t\tSEVERITY_MAJOR)\n \t\t\tw.WriteHeader(http.StatusForbidden)\n-\t\t\tw.Write([]byte(err.Error()))\n+\t\t\tif _, err := w.Write([]byte(err.Error())); err != nil {\n+\t\t\t\tlog.Error(err)\n+\t\t\t}\n \t\t}\n \t} else {\n+\t\tIncRequestErrorCounter(\"forbidden\", useremail, action, r.URL.Path,\n+\t\t\tSEVERITY_MINOR)\n \t\tw.WriteHeader(http.StatusForbidden)\n \t}\n }\n \n func (c *KfamV1Alpha1Client) CreateProfile(w http.ResponseWriter, r *http.Request) {\n \tw.Header().Set(\"Content-Type\", \"application/json; charset=UTF-8\")\n+\tconst action = \"create\"\n \tvar profile profilev1beta1.Profile\n \tif err := json.NewDecoder(r.Body).Decode(&profile); err != nil {\n-\t\tjson.NewEncoder(w).Encode(err)\n+\t\tIncRequestErrorCounter(\"decode error\", \"\", action, r.URL.Path,\n+\t\t\tSEVERITY_MAJOR)\n+\t\tif err := json.NewEncoder(w).Encode(err); err != nil {\n+\t\t\tlog.Error(err)\n+\t\t}\n \t\tw.WriteHeader(http.StatusForbidden)\n \t\treturn\n \t}\n \t_, err := c.profileClient.Create(&profile)\n \tif err == nil {\n+\t\tIncRequestCounter(\"\", \"\", action, r.URL.Path)\n \t\tw.WriteHeader(http.StatusOK)\n \t} else {\n+\t\tIncRequestErrorCounter(err.Error(), \"\", action, r.URL.Path,\n+\t\t\tSEVERITY_MAJOR)\n \t\tw.WriteHeader(http.StatusForbidden)\n-\t\tw.Write([]byte(err.Error()))\n+\t\tif _, err := w.Write([]byte(err.Error())); err != nil {\n+\t\t\tlog.Error(err)",
        "comment_created_at": "2020-01-21T21:58:53+00:00",
        "comment_author": "zhenghuiwang",
        "comment_body": "Couple of suggestions for error handling in this case and other similar cases:\r\n\r\n1. There are two variables both named `err` here with different scopes. I would suggest using two different names to make it clear which error is used, like `err` & `e`.\r\n\r\n2. The `log.Error(err)` refers to the error of failing to write the response bytes. Besides this, the error message of status forbidden(non-OK response) also worth logging on server side.\r\n\r\n3. Consider wrapping the context of errors for future debugging, such as\r\n```\r\nlog.Error(fmt.Errorf(\"Request for profile %s is forbidden: %v\", action, err))\r\nlog.Error(fmt.Errorf(\"Internal server error: failed to write response bytes: %v\", e))\r\n```\r\nThere are libraries for wrapping error in more structured way.\r\n  ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "320266099",
    "pr_number": 4040,
    "pr_file": "bootstrap/cmd/kfctl/cmd/apply.go",
    "created_at": "2019-09-03T13:18:13+00:00",
    "commented_code": "if resourceErr != nil {\n\t\t\treturn fmt.Errorf(\"invalid resource: %v\", resourceErr)",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "320266099",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 4040,
        "pr_file": "bootstrap/cmd/kfctl/cmd/apply.go",
        "discussion_id": "320266099",
        "commented_code": "@@ -39,7 +45,19 @@ var applyCmd = &cobra.Command{\n \t\tif resourceErr != nil {\n \t\t\treturn fmt.Errorf(\"invalid resource: %v\", resourceErr)",
        "comment_created_at": "2019-09-03T13:18:13+00:00",
        "comment_author": "yanniszark",
        "comment_body": "I believe we want to return a KFError everywhere.\r\nCheck out how the coordinator does it: https://github.com/kubeflow/kubeflow/blob/7d976050933d642069591b72138eb3c152224d08/bootstrap/pkg/kfapp/coordinator/coordinator.go#L79\r\n\r\nIdeally, we could make a helper function `NewInternalKFError(e error, msg string)` in `pkg/apis/kferrors.go` to reduce boilerplate.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "322854742",
    "pr_number": 4040,
    "pr_file": "bootstrap/cmd/kfctl/cmd/apply/apply.go",
    "created_at": "2019-09-10T16:53:36+00:00",
    "commented_code": "package apply\n\nimport (\n\t\"errors\"\n\t\"fmt\"\n\t\"io\"\n\t\"os\"\n\n\tkfapis \"github.com/kubeflow/kubeflow/bootstrap/v3/pkg/apis\"\n\tkftypes \"github.com/kubeflow/kubeflow/bootstrap/v3/pkg/apis/apps\"\n\tkfdefsv3 \"github.com/kubeflow/kubeflow/bootstrap/v3/pkg/apis/apps/kfdef/v1alpha1\"\n\t\"github.com/kubeflow/kubeflow/bootstrap/v3/pkg/kfapp/coordinator\"\n\tlog \"github.com/sirupsen/logrus\"\n)\n\n// Set default app name to kf-app\nconst appName = \"kf-app\"\n\nvar kfErr = &kfapis.KfError{\n\tCode:    int(kfapis.INTERNAL_ERROR),",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "322854742",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 4040,
        "pr_file": "bootstrap/cmd/kfctl/cmd/apply/apply.go",
        "discussion_id": "322854742",
        "commented_code": "@@ -0,0 +1,112 @@\n+package apply\n+\n+import (\n+\t\"errors\"\n+\t\"fmt\"\n+\t\"io\"\n+\t\"os\"\n+\n+\tkfapis \"github.com/kubeflow/kubeflow/bootstrap/v3/pkg/apis\"\n+\tkftypes \"github.com/kubeflow/kubeflow/bootstrap/v3/pkg/apis/apps\"\n+\tkfdefsv3 \"github.com/kubeflow/kubeflow/bootstrap/v3/pkg/apis/apps/kfdef/v1alpha1\"\n+\t\"github.com/kubeflow/kubeflow/bootstrap/v3/pkg/kfapp/coordinator\"\n+\tlog \"github.com/sirupsen/logrus\"\n+)\n+\n+// Set default app name to kf-app\n+const appName = \"kf-app\"\n+\n+var kfErr = &kfapis.KfError{\n+\tCode:    int(kfapis.INTERNAL_ERROR),",
        "comment_created_at": "2019-09-10T16:53:36+00:00",
        "comment_author": "gabrielwen",
        "comment_body": "are all errors internal errors?  internal errors mean there is something wrong with `kfctl` and we need to fix it.  shouldn't part of errors be invalid arguments?",
        "pr_file_module": null
      },
      {
        "comment_id": "323031180",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 4040,
        "pr_file": "bootstrap/cmd/kfctl/cmd/apply/apply.go",
        "discussion_id": "322854742",
        "commented_code": "@@ -0,0 +1,112 @@\n+package apply\n+\n+import (\n+\t\"errors\"\n+\t\"fmt\"\n+\t\"io\"\n+\t\"os\"\n+\n+\tkfapis \"github.com/kubeflow/kubeflow/bootstrap/v3/pkg/apis\"\n+\tkftypes \"github.com/kubeflow/kubeflow/bootstrap/v3/pkg/apis/apps\"\n+\tkfdefsv3 \"github.com/kubeflow/kubeflow/bootstrap/v3/pkg/apis/apps/kfdef/v1alpha1\"\n+\t\"github.com/kubeflow/kubeflow/bootstrap/v3/pkg/kfapp/coordinator\"\n+\tlog \"github.com/sirupsen/logrus\"\n+)\n+\n+// Set default app name to kf-app\n+const appName = \"kf-app\"\n+\n+var kfErr = &kfapis.KfError{\n+\tCode:    int(kfapis.INTERNAL_ERROR),",
        "comment_created_at": "2019-09-11T01:57:05+00:00",
        "comment_author": "swiftdiaries",
        "comment_body": "Added a bunch of Invalid argument errors for when appropriate.",
        "pr_file_module": null
      }
    ]
  }
]
