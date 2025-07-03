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
