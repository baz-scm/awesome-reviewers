---
title: Manage Session Lifecycles
description: To optimize performance and avoid wasted compute (vCPU/memory), ensure
  AgentCore sessions end promptly—either by setting an appropriate idle timeout or
  by explicitly stopping the session when work is complete.
repository: awslabs/agentcore-samples
label: Performance Optimization
language: Other
comments_count: 2
repository_stars: 3244
---

To optimize performance and avoid wasted compute (vCPU/memory), ensure AgentCore sessions end promptly—either by setting an appropriate idle timeout or by explicitly stopping the session when work is complete.

Apply this standard:
1) Configure an idle timeout during runtime/session setup so inactive sessions are automatically terminated.
2) When a user/job finishes, call `stop_runtime_session` for that specific session to immediately release microVM resources while keeping the runtime ready for new sessions.

Example (stop a completed session + set a shorter idle timeout):

```python
# 1) Stop a specific session when done
if runtime_session_id:
    agentcore_client.stop_runtime_session(
        agentRuntimeArn=agent_arn,
        runtimeSessionId=runtime_session_id,
        qualifier='DEFAULT'
    )

# 2) Update runtime to automatically terminate idle sessions
agentcore_control_client = boto3.client('bedrock-agentcore-control', region_name=region)
agentcore_control_client.update_agent_runtime(
    agentRuntimeId=launch_result_short.agent_id,
    lifecycleConfiguration={
        'idleRuntimeSessionTimeout': 300  # 5 minutes (tune per workload)
    }
)
```

Choose idle timeouts based on use case (shorter for development/testing; longer for interactive production workloads) to balance responsiveness and resource utilization.