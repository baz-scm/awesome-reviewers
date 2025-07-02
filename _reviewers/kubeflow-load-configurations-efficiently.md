---
title: Load configurations efficiently
description: 'When designing components that require configuration, follow these practices
  to enhance performance, maintainability, and usability:


  1. **Load configuration once at startup** rather than repeatedly during reconciliation
  loops:'
repository: kubeflow/kubeflow
label: Configurations
language: Go
comments_count: 4
repository_stars: 15064
---

When designing components that require configuration, follow these practices to enhance performance, maintainability, and usability:

1. **Load configuration once at startup** rather than repeatedly during reconciliation loops:
```go
// Good: Load at controller initialization
func NewMyController() *MyController {
    // Load config once when controller starts
    config, err := loadConfigFromFile(configPath)
    if err != nil {
        // Handle error or fail fast
    }
    return &MyController{config: config}
}

// Avoid: Loading in reconcile loop
func (r *MyController) Reconcile() {
    // Don't do this - performance issue
    config, _ := loadConfigFromFile(configPath) 
    // ...
}
```

2. **Use standard formats** (YAML/JSON) with established libraries instead of creating custom parsers:
```go
// Good: Use standard libraries
import "github.com/go-yaml/yaml"

func loadConfig(file string) (Config, error) {
    var config Config
    data, err := os.ReadFile(file)
    if err != nil {
        return config, err
    }
    return config, yaml.Unmarshal(data, &config)
}

// Avoid: Custom parsing logic
func parseConfig(file string) {
    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        line := scanner.Text()
        // Custom parsing logic is harder to maintain
    }
}
```

3. **Don't hardcode configuration paths** - provide reasonable defaults but allow overriding via command line arguments:
```go
// Good: Make path configurable
var configPath = flag.String("config", "/etc/default/config.yaml", "Path to configuration file")

func main() {
    flag.Parse()
    config, err := loadConfig(*configPath)
    // ...
}
```

4. **Set sensible defaults** for configuration values but provide clear ways to override them through explicit configuration.

These practices help avoid reinventing parsing logic, improve performance by reducing unnecessary I/O operations, and make your components more configurable across different environments.


[
  {
    "discussion_id": "600238600",
    "pr_number": 5761,
    "pr_file": "components/profile-controller/controllers/profile_controller.go",
    "created_at": "2021-03-24T07:44:10+00:00",
    "commented_code": "return\n}\n\nfunc mergeLabelPropertiesToMap(logger logr.Logger) {\n\tfile, err := os.Open(NAMESPACE_LABELS_PROPERTIES)\n\tif err != nil {\n\t\tlogger.Info(\"namespace labels properties file doesn't exist, using default value\")\n\t}\n\tdefer file.Close()\n\n\tscanner := bufio.NewScanner(file)\n\tfor scanner.Scan() {\n\t\tlabel := scanner.Text()\n\t\tarr := strings.Split(label, \"=\")\n\t\tif len(arr) > 2 || len(arr) == 0 {\n\t\t\tlogger.Info(\"label config format incorrect, should be {key}={value}\", \"label\", label)\n\t\t} else {\n\t\t\tif arr[0] == \"\" {\n\t\t\t\tlogger.Info(\"label key should not be empty\", \"label\", label)\n\t\t\t} else if len(arr) == 2 {\n\t\t\t\t// Add or overwrite label map if value exists.\n\t\t\t\tkubeflowNamespaceLabels[arr[0]] = arr[1]\n\t\t\t} else {\n\t\t\t\t// Set value to be empty if nothing exists after \"=\".\n\t\t\t\t// It means this label needs to be removed.\n\t\t\t\tkubeflowNamespaceLabels[arr[0]] = \"\"\n\t\t\t}\n\t\t}\n\t}",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "600238600",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5761,
        "pr_file": "components/profile-controller/controllers/profile_controller.go",
        "discussion_id": "600238600",
        "commented_code": "@@ -616,15 +624,59 @@ func removeString(slice []string, s string) (result []string) {\n \treturn\n }\n \n+func mergeLabelPropertiesToMap(logger logr.Logger) {\n+\tfile, err := os.Open(NAMESPACE_LABELS_PROPERTIES)\n+\tif err != nil {\n+\t\tlogger.Info(\"namespace labels properties file doesn't exist, using default value\")\n+\t}\n+\tdefer file.Close()\n+\n+\tscanner := bufio.NewScanner(file)\n+\tfor scanner.Scan() {\n+\t\tlabel := scanner.Text()\n+\t\tarr := strings.Split(label, \"=\")\n+\t\tif len(arr) > 2 || len(arr) == 0 {\n+\t\t\tlogger.Info(\"label config format incorrect, should be {key}={value}\", \"label\", label)\n+\t\t} else {\n+\t\t\tif arr[0] == \"\" {\n+\t\t\t\tlogger.Info(\"label key should not be empty\", \"label\", label)\n+\t\t\t} else if len(arr) == 2 {\n+\t\t\t\t// Add or overwrite label map if value exists.\n+\t\t\t\tkubeflowNamespaceLabels[arr[0]] = arr[1]\n+\t\t\t} else {\n+\t\t\t\t// Set value to be empty if nothing exists after \"=\".\n+\t\t\t\t// It means this label needs to be removed.\n+\t\t\t\tkubeflowNamespaceLabels[arr[0]] = \"\"\n+\t\t\t}\n+\t\t}\n+\t}",
        "comment_created_at": "2021-03-24T07:44:10+00:00",
        "comment_author": "Bobgy",
        "comment_body": "It's a nice implementation of the syntax you are proposing.\r\n\r\nHowever, it seems a little unnecessary if we can just use YAML format as the config format, so people do not need to reinvent the wheels and consumers won't guess about how the format is parsed. There are standard libraries for parsing YAML in go: https://github.com/go-yaml/yaml/tree/v2.\r\n\r\nUsing the standards mean that e.g. it's very easy to insert comments in the configfile, without you needing to implement logic to ignore comments.",
        "pr_file_module": null
      },
      {
        "comment_id": "600794348",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5761,
        "pr_file": "components/profile-controller/controllers/profile_controller.go",
        "discussion_id": "600238600",
        "commented_code": "@@ -616,15 +624,59 @@ func removeString(slice []string, s string) (result []string) {\n \treturn\n }\n \n+func mergeLabelPropertiesToMap(logger logr.Logger) {\n+\tfile, err := os.Open(NAMESPACE_LABELS_PROPERTIES)\n+\tif err != nil {\n+\t\tlogger.Info(\"namespace labels properties file doesn't exist, using default value\")\n+\t}\n+\tdefer file.Close()\n+\n+\tscanner := bufio.NewScanner(file)\n+\tfor scanner.Scan() {\n+\t\tlabel := scanner.Text()\n+\t\tarr := strings.Split(label, \"=\")\n+\t\tif len(arr) > 2 || len(arr) == 0 {\n+\t\t\tlogger.Info(\"label config format incorrect, should be {key}={value}\", \"label\", label)\n+\t\t} else {\n+\t\t\tif arr[0] == \"\" {\n+\t\t\t\tlogger.Info(\"label key should not be empty\", \"label\", label)\n+\t\t\t} else if len(arr) == 2 {\n+\t\t\t\t// Add or overwrite label map if value exists.\n+\t\t\t\tkubeflowNamespaceLabels[arr[0]] = arr[1]\n+\t\t\t} else {\n+\t\t\t\t// Set value to be empty if nothing exists after \"=\".\n+\t\t\t\t// It means this label needs to be removed.\n+\t\t\t\tkubeflowNamespaceLabels[arr[0]] = \"\"\n+\t\t\t}\n+\t\t}\n+\t}",
        "comment_created_at": "2021-03-24T19:08:28+00:00",
        "comment_author": "zijianjoy",
        "comment_body": "Thank you for the suggestion! I have switched to yaml format in new commit.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "600239852",
    "pr_number": 5761,
    "pr_file": "components/profile-controller/controllers/profile_controller.go",
    "created_at": "2021-03-24T07:46:37+00:00",
    "commented_code": "return\n}\n\nfunc mergeLabelPropertiesToMap(logger logr.Logger) {\n\tfile, err := os.Open(NAMESPACE_LABELS_PROPERTIES)",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "600239852",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5761,
        "pr_file": "components/profile-controller/controllers/profile_controller.go",
        "discussion_id": "600239852",
        "commented_code": "@@ -616,15 +624,59 @@ func removeString(slice []string, s string) (result []string) {\n \treturn\n }\n \n+func mergeLabelPropertiesToMap(logger logr.Logger) {\n+\tfile, err := os.Open(NAMESPACE_LABELS_PROPERTIES)",
        "comment_created_at": "2021-03-24T07:46:37+00:00",
        "comment_author": "Bobgy",
        "comment_body": "A controller runs in reconcile loops, this method is called very very often, so it'd be better to load the config file at controller startup and fail the controller if any errors show up.",
        "pr_file_module": null
      },
      {
        "comment_id": "600795933",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5761,
        "pr_file": "components/profile-controller/controllers/profile_controller.go",
        "discussion_id": "600239852",
        "commented_code": "@@ -616,15 +624,59 @@ func removeString(slice []string, s string) (result []string) {\n \treturn\n }\n \n+func mergeLabelPropertiesToMap(logger logr.Logger) {\n+\tfile, err := os.Open(NAMESPACE_LABELS_PROPERTIES)",
        "comment_created_at": "2021-03-24T19:10:02+00:00",
        "comment_author": "zijianjoy",
        "comment_body": "If the configmap is updated, we want to read from the latest data instead of cache for label configuration. So we will need to read from VolumeMount. Is it very resource intense to read a file? If yes, what is your suggestion of reading new ConfigMap data?",
        "pr_file_module": null
      },
      {
        "comment_id": "600933543",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5761,
        "pr_file": "components/profile-controller/controllers/profile_controller.go",
        "discussion_id": "600239852",
        "commented_code": "@@ -616,15 +624,59 @@ func removeString(slice []string, s string) (result []string) {\n \treturn\n }\n \n+func mergeLabelPropertiesToMap(logger logr.Logger) {\n+\tfile, err := os.Open(NAMESPACE_LABELS_PROPERTIES)",
        "comment_created_at": "2021-03-24T23:11:05+00:00",
        "comment_author": "Bobgy",
        "comment_body": "Note this is a controller, not a service. It's not a big deal to restart an instance to update configs.\n\nRegarding live configmap refresh, I believe there is a config library -- viper which KFP is using too, it can be set-up to watch file/configmap changes, however I think that's not worth the complexity.",
        "pr_file_module": null
      },
      {
        "comment_id": "604343502",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5761,
        "pr_file": "components/profile-controller/controllers/profile_controller.go",
        "discussion_id": "600239852",
        "commented_code": "@@ -616,15 +624,59 @@ func removeString(slice []string, s string) (result []string) {\n \treturn\n }\n \n+func mergeLabelPropertiesToMap(logger logr.Logger) {\n+\tfile, err := os.Open(NAMESPACE_LABELS_PROPERTIES)",
        "comment_created_at": "2021-03-30T18:38:31+00:00",
        "comment_author": "zijianjoy",
        "comment_body": "Thank you for confirming! I think it makes sense and updated the code to reflect one-time file read. I would love to learn about viper later on.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "600240614",
    "pr_number": 5761,
    "pr_file": "components/profile-controller/controllers/profile_controller.go",
    "created_at": "2021-03-24T07:48:03+00:00",
    "commented_code": "const ROLE = \"role\"\nconst ADMIN = \"admin\"\n\n// External input for labels to be added to namespace.\nconst NAMESPACE_LABELS_PROPERTIES = \"/etc/config/labels/namespace-labels.properties\"",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "600240614",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5761,
        "pr_file": "components/profile-controller/controllers/profile_controller.go",
        "discussion_id": "600240614",
        "commented_code": "@@ -55,6 +58,9 @@ const USER = \"user\"\n const ROLE = \"role\"\n const ADMIN = \"admin\"\n \n+// External input for labels to be added to namespace.\n+const NAMESPACE_LABELS_PROPERTIES = \"/etc/config/labels/namespace-labels.properties\"",
        "comment_created_at": "2021-03-24T07:48:03+00:00",
        "comment_author": "Bobgy",
        "comment_body": "it's not a good practice to hard-code config file location, it's reasonable to specify a default location, but the default location should typically be overridable from a command line argument.",
        "pr_file_module": null
      },
      {
        "comment_id": "600796354",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5761,
        "pr_file": "components/profile-controller/controllers/profile_controller.go",
        "discussion_id": "600240614",
        "commented_code": "@@ -55,6 +58,9 @@ const USER = \"user\"\n const ROLE = \"role\"\n const ADMIN = \"admin\"\n \n+// External input for labels to be added to namespace.\n+const NAMESPACE_LABELS_PROPERTIES = \"/etc/config/labels/namespace-labels.properties\"",
        "comment_created_at": "2021-03-24T19:10:29+00:00",
        "comment_author": "zijianjoy",
        "comment_body": "Make sense, I changed it to a CLI argument with default value. Thank you!",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "332201398",
    "pr_number": 4244,
    "pr_file": "bootstrap/pkg/kfapp/coordinator/coordinator.go",
    "created_at": "2019-10-07T19:42:49+00:00",
    "commented_code": "// kftypesv3.LoadKfApp which will try and dynamically load a .so\n//\nfunc getPackageManager(kfdef *kfdefsv3.KfDef) (kftypesv3.KfApp, error) {\n\tswitch kfdef.Spec.PackageManager {\n\n\tpackageManager := kfdef.Spec.PackageManager",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "332201398",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 4244,
        "pr_file": "bootstrap/pkg/kfapp/coordinator/coordinator.go",
        "discussion_id": "332201398",
        "commented_code": "@@ -142,7 +142,13 @@ func (coord *coordinator) getPackageManagers(kfdef *kfdefsv3.KfDef) *map[string]\n // kftypesv3.LoadKfApp which will try and dynamically load a .so\n //\n func getPackageManager(kfdef *kfdefsv3.KfDef) (kftypesv3.KfApp, error) {\n-\tswitch kfdef.Spec.PackageManager {\n+\n+\tpackageManager := kfdef.Spec.PackageManager",
        "comment_created_at": "2019-10-07T19:42:49+00:00",
        "comment_author": "jlewi",
        "comment_body": "Shouldn't the defaults be filled in before we call getPackageManager? Specifically when we call NewKfApp\r\nhttps://github.com/kubeflow/kubeflow/blob/2395c5fc0d384cf6dd4d7167bbe9010cd1315b54/bootstrap/pkg/kfapp/coordinator/coordinator.go#L468\r\n\r\nIsn't that where any initialization code that sets default values should happen? So that's where we could set PackageManager to Kustomize.",
        "pr_file_module": null
      },
      {
        "comment_id": "332471183",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 4244,
        "pr_file": "bootstrap/pkg/kfapp/coordinator/coordinator.go",
        "discussion_id": "332201398",
        "commented_code": "@@ -142,7 +142,13 @@ func (coord *coordinator) getPackageManagers(kfdef *kfdefsv3.KfDef) *map[string]\n // kftypesv3.LoadKfApp which will try and dynamically load a .so\n //\n func getPackageManager(kfdef *kfdefsv3.KfDef) (kftypesv3.KfApp, error) {\n-\tswitch kfdef.Spec.PackageManager {\n+\n+\tpackageManager := kfdef.Spec.PackageManager",
        "comment_created_at": "2019-10-08T11:58:12+00:00",
        "comment_author": "yanniszark",
        "comment_body": "@jlewi `NewKfApp` isn't used anymore.\r\nI don't think we have a clear way of doing defaulting right now.\r\nRight now we have the following call chains:\r\n\r\nbuild: `BuildKfAppFromURI` -> `NewLoadKfAppFromURI` which loads a KfDef (`LoadKFDefFromURI`), persists it as app.yaml (`CreateKfAppCfgFile`) and then loads it (`LoadKfAppCfgFile`).\r\napply: `LoadKfAppCfgFile`\r\n\r\nIMO it makes most sense to have it inside `NewLoadKfAppFromURI`, I see that there are also some GCP checks in there.",
        "pr_file_module": null
      },
      {
        "comment_id": "332499138",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 4244,
        "pr_file": "bootstrap/pkg/kfapp/coordinator/coordinator.go",
        "discussion_id": "332201398",
        "commented_code": "@@ -142,7 +142,13 @@ func (coord *coordinator) getPackageManagers(kfdef *kfdefsv3.KfDef) *map[string]\n // kftypesv3.LoadKfApp which will try and dynamically load a .so\n //\n func getPackageManager(kfdef *kfdefsv3.KfDef) (kftypesv3.KfApp, error) {\n-\tswitch kfdef.Spec.PackageManager {\n+\n+\tpackageManager := kfdef.Spec.PackageManager",
        "comment_created_at": "2019-10-08T13:05:21+00:00",
        "comment_author": "jlewi",
        "comment_body": "Doing it in the new functions seems better. Since we have multiple entry points I might suggest creating a new function \"initDefaults\" or something like that, that can be called from multiple entry points if needed.\r\n\r\n",
        "pr_file_module": null
      }
    ]
  }
]
