---
title: Test actual functionality
description: Ensure tests verify real operations and integration scenarios rather
  than just basic concepts or type definitions. Many test suites contain placeholder
  tests that only check if functions exist or verify simple type structures, but fail
  to test the actual behavior and interactions that matter in production.
repository: cloudflare/agents
label: Testing
language: TypeScript
comments_count: 6
repository_stars: 2312
---

Ensure tests verify real operations and integration scenarios rather than just basic concepts or type definitions. Many test suites contain placeholder tests that only check if functions exist or verify simple type structures, but fail to test the actual behavior and interactions that matter in production.

Tests should cover:
- Real operations (SQL queries, queue processing, RPC calls) not just type definitions
- Integration scenarios (multi-client state synchronization, server interactions)
- Preferred API patterns that the team wants developers to use
- Context-dependent functionality across different execution environments

Example of inadequate testing:
```typescript
it("should understand queue concepts", () => {
  type QueueItem = { id: string; callback: string; payload: unknown; };
  const testQueueItem: QueueItem = { id: "queue-123", callback: "processData", payload: { data: "test" } };
  expect(testQueueItem.id).toBeDefined(); // Only tests type structure
});
```

Example of proper functional testing:
```typescript
it("should process queue items and handle retries", async () => {
  const agent = await getAgentByName(env.TEST_AGENT, "queue-test");
  
  // Test actual queue operations
  await agent.enqueue("processData", { data: "test" });
  const result = await agent.processQueue();
  
  expect(result.processed).toBe(1);
  expect(result.failed).toBe(0);
});

it("should sync state between multiple clients", async () => {
  const client1 = new AgentClient({ agent: "TestAgent", name: "client1" });
  const client2 = new AgentClient({ agent: "TestAgent", name: "client2" });
  
  const client2Updates = [];
  client2.onStateUpdate = (state) => client2Updates.push(state);
  
  client1.setState({ count: 5 });
  
  // Verify real multi-client synchronization
  expect(client2Updates).toContainEqual({ count: 5 });
});
```

This approach ensures tests provide meaningful coverage of how systems actually behave in production rather than just verifying that code compiles or basic structures exist.