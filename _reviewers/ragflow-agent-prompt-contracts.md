---
title: Agent Prompt Contracts
description: 'When building LLM Agents, treat the system prompt + framework prompt
  blocks as a contract with the agent’s inputs and tool/sub-agent configuration.


  Apply these rules:'
repository: infiniflow/ragflow
label: AI
language: Other
comments_count: 3
repository_stars: 80174
---

When building LLM Agents, treat the system prompt + framework prompt blocks as a contract with the agent’s inputs and tool/sub-agent configuration.

Apply these rules:
- Bind required variables: an Agent’s data inputs come from keys (variables) that must be used together with the system prompt. In practice, open the key list (e.g., `/` or the **(x)** button) and ensure every variable referenced by the prompt/framework blocks is supplied.
- Use framework blocks with the expected inputs: for example, `task_analysis` should receive `agent_prompt`, `task`, `tool_desc`, and `context`, and `plan_generation` should generate the next execution plan from `task_analysis` results.
- Make tool usage deterministic: if tools are available, specify in the prompt what kinds of tasks should trigger which tools.
- Don’t assume “lead agent only” activation: framework prompt blocks should appear/operate when an Agent has Tools or Subagents configured (verify by checking the **Framework** dropdown after configuring Tools/Subagents), and ensure subagent delegation keeps the prompt contract intact.

Example pattern (conceptual):
```text
System prompt (with variables):
- Role + instructions
- Tool policy: “Use Tool A for classification/summarization; use Tool B for retrieval; otherwise ask a clarifying question.”

Framework blocks:
- task_analysis(agent_prompt, task, tool_desc, context) -> produces structured analysis
- plan_generation(...) -> creates the next steps based on that analysis

Keys:
- Provide all variables referenced by system prompt/framework blocks.
- Confirm required keys exist via the keys UI (/ or (x)).
```