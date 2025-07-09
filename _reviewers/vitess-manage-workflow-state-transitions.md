---
title: Manage workflow state transitions
description: When working with temporal workflows, always implement explicit state
  transitions rather than abrupt deletions. Workflows should proceed through well-defined
  states (like running, stopped, or frozen) to ensure proper lifecycle management
  and durable execution.
repository: vitessio/vitess
label: Temporal
language: Go
comments_count: 2
repository_stars: 19815
---

When working with temporal workflows, always implement explicit state transitions rather than abrupt deletions. Workflows should proceed through well-defined states (like running, stopped, or frozen) to ensure proper lifecycle management and durable execution.

Instead of directly deleting workflows:
```go
// Not recommended
if _, derr := s.WorkflowDelete(ctx, &vtctldatapb.WorkflowDeleteRequest{
    Keyspace:         req.TableKeyspace,
    Workflow:         req.Name,
    KeepData:         true,
    KeepRoutingRules: true,
}); derr != nil {
    return nil, vterrors.Errorf(vtrpcpb.Code_FAILED_PRECONDITION, "failed to delete workflow %s: %v", req.Name, derr)
}
```

Implement proper state transitions:
```go
// Recommended
// First stop the workflow
_, err = s.tmc.UpdateVReplicationWorkflow(ctx, tabletInfo.Tablet, &tabletmanagerdatapb.UpdateVReplicationWorkflowRequest{
    Workflow: req.Name,
    State:    ptr.Of(binlogdatapb.VReplicationWorkflowState_Stopped),
})
if err != nil {
    return vterrors.Wrapf(err, "failed to stop workflow %s on shard %s/%s", req.Name, tabletInfo.Keyspace, tabletInfo.Shard)
}
// Then mark workflow as frozen
query := fmt.Sprintf(SqlFreezeWorkflow, Frozen, encodeString(tabletInfo.DbName()), encodeString(req.Name))
_, err = s.tmc.VReplicationExec(ctx, tabletInfo.Tablet, query)
```

Commands that operate on workflows should check and enforce preconditions related to workflow state. As seen in the discussion about `complete` and `cancel` commands, make sure each command has clear semantics regarding workflow state requirements.