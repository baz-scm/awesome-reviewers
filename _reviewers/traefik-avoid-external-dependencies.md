---
title: avoid external dependencies
description: Unit tests should not depend on external components like databases, Redis,
  or Kubernetes clusters. Instead, create fake implementations or use mocks to isolate
  the code under test. Reserve integration tests for scenarios that require real external
  services.
repository: traefik/traefik
label: Testing
language: Go
comments_count: 2
repository_stars: 55772
---

Unit tests should not depend on external components like databases, Redis, or Kubernetes clusters. Instead, create fake implementations or use mocks to isolate the code under test. Reserve integration tests for scenarios that require real external services.

When testing against external components is necessary, implement fake clients that simulate the external service behavior. For example, when testing Redis rate limiting:

```go
type FakeRedisClient struct{
	script string
	keys   *ttlmap.TtlMap
}

func (m FakeRedisClient) EvalSha(ctx context.Context, _ string, keys []string, args ...interface{}) *redis.Cmd {
	state := lua.NewState()
	defer state.Close()
	
	// Set up Lua environment with KEYS and ARGV
	tableKeys := state.NewTable()
	for _, key := range keys {
		tableKeys.Append(lua.LString(key))
	}
	state.SetGlobal("KEYS", tableKeys)
	
	// Implement Redis commands like GET, SET
	mod := state.SetFuncs(state.NewTable(), map[string]lua.LGFunction{
		"call": func(state *lua.LState) int {
			switch state.Get(1).String() {
			case "GET":
				key := state.Get(2).String()
				value, ok := m.keys.Get(key)
				if !ok {
					state.Push(lua.LNil)
				} else {
					state.Push(lua.LString(value.(string)))
				}
			case "SET":
				// Handle SET operations
			}
			return 1
		},
	})
	state.SetGlobal("redis", mod)
	
	// Execute and return result
	cmd := redis.NewCmd(ctx)
	// ... execute Lua script and set result
	return cmd
}
```

This approach keeps unit tests fast, reliable, and independent while still validating the core logic. Use integration tests in the `integration` directory when you need to verify behavior against actual external services.