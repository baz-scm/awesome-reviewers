---
title: Explicit dependency graph
description: When implementing algorithms involving dependencies between components
  or operations, model the dependency graph explicitly rather than relying on implicit
  ordering. Explicit graph modeling facilitates cycle detection, enables parallel
  execution of independent operations, and provides clear visualization of relationships
  between components.
repository: hashicorp/terraform
label: Algorithms
language: Go
comments_count: 2
repository_stars: 45532
---

When implementing algorithms involving dependencies between components or operations, model the dependency graph explicitly rather than relying on implicit ordering. Explicit graph modeling facilitates cycle detection, enables parallel execution of independent operations, and provides clear visualization of relationships between components.

Key practices:
1. Create distinct nodes for each component or operation
2. Connect nodes with directional edges based on dependencies
3. Implement specific logic for handling parallel vs. sequential execution
4. Include cycle detection in traversal operations

Example:
```go
// Create nodes for each operation
for _, operation := range operations {
    node := &OperationNode{operation: operation}
    graph.Add(node)
    nodes = append(nodes, node)
}

// Connect nodes based on dependencies
for _, node := range nodes {
    // Connect based on explicit dependencies
    for _, dep := range node.operation.Dependencies() {
        dependencyNode := findNodeByID(nodes, dep)
        if dependencyNode != nil {
            graph.Connect(dag.BasicEdge(node, dependencyNode))
        }
    }
    
    // Connect parallel/sequential operations appropriately
    if !node.operation.IsParallel() {
        // Non-parallel operations should depend on all previous parallel operations
        for _, prev := range previousParallelNodes {
            graph.Connect(dag.BasicEdge(node, prev))
        }
    }
}

// Check for cycles during validation
if cycles := graph.Cycles(); len(cycles) > 0 {
    return fmt.Errorf("dependency cycles detected: %v", cycles)
}
```

By explicitly modeling dependencies, you create a more maintainable and robust system that can handle complex execution patterns while preventing circular dependencies.