---
title: Conversation context fidelity
description: When an agent's prompt or task text implicitly refers to conversation
  state (e.g. "the conversation above", "the judge's evaluation is in the conversation
  above"), the code must guarantee that referenced state actually exists, is complete,
  and is correctly scoped before the call is made. Several bugs in multi-agent orchestration
  code (debate loops,...
repository: kyegomez/swarms#pi240310
label: AI
language: Python
comments_count: 8
repository_stars: 7337
---

When an agent's prompt or task text implicitly refers to conversation state (e.g. "the conversation above", "the judge's evaluation is in the conversation above"), the code must guarantee that referenced state actually exists, is complete, and is correctly scoped before the call is made. Several bugs in multi-agent orchestration code (debate loops, planners, councils, round-robin, hierarchical directors) stemmed from this contract being silently broken:

- Prompts asserting content is "above" with no check that `messages_for`/the built message list is non-empty, so an empty or filtered context causes hallucinated or refused responses instead of a clear failure.
- Shared conversation objects not reset between independent `run()` invocations, leaking a prior task's turns into a new task's context.
- History-slicing helpers (e.g. `split_last_turn`) reused from another component without re-deriving the invariant they encode, silently dropping the most recent turn an agent was supposed to build on.
- Caller-supplied agents (e.g. a custom director) getting a tool/schema attached without the matching system prompt, so they have capability but not the instructions needed to use it correctly.
- Loop/status notes written to a transcript but not mirrored into persisted memory, so what the model saw during inference diverges from what gets saved/replayed later.

To apply this standard:
1. Before sending a prompt that references prior context, assert or guard that the context is non-empty and contains what the prompt claims (or word the prompt defensively, e.g. "using any prior conversation" instead of asserting it exists).
2. Reset or scope shared conversation/memory state per logical run so independent invocations never see each other's turns.
3. When slicing or filtering message history before passing it to an agent, verify that the slice includes every turn the next prompt depends on (don't blindly copy a slicing pattern from another component).
4. When attaching capabilities (tools/schemas) to an externally supplied agent, also attach or verify the instructions needed to use them correctly.
5. Keep persisted memory and the actual model-visible transcript in sync — any note/content added to the prompt context must also be written to memory (or vice versa), so saved state reflects what was actually inferred over.

Example guard before a context-dependent prompt:
```python
prior_turns = messages_for(agent.agent_name, self.conversation)
if not prior_turns:
    task = "No prior conversation yet. " + base_task
else:
    task = "Using the prior conversation, " + base_task
agent.run(task=task, messages=prior_turns)
```