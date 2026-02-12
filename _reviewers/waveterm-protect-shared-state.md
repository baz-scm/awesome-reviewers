---
title: Protect shared state
description: Ensure mutable shared data is never exposed or accessed without explicit
  synchronization. When data crosses goroutine boundaries you must either copy it,
  provide a concurrency-safe accessor that returns a snapshot, or protect it with
  proper synchronization (mutexes, atomics, or reference counting). This prevents
  races when marshaling, iterating, or doing...
repository: wavetermdev/waveterm
label: Concurrency
language: Go
comments_count: 8
repository_stars: 17328
---

Ensure mutable shared data is never exposed or accessed without explicit synchronization. When data crosses goroutine boundaries you must either copy it, provide a concurrency-safe accessor that returns a snapshot, or protect it with proper synchronization (mutexes, atomics, or reference counting). This prevents races when marshaling, iterating, or doing read-modify-write updates.

Guidelines (practical):
- Return copies for internal maps/structs or provide an accessor that returns a copied snapshot. e.g.:
  func (m *MShellProc) GetRemoteRuntimeState() RemoteRuntimeState {
      varsCopy := make(map[string]string)
      for k,v := range m.Remote.StateVars { // hold m lock while reading
          varsCopy[k] = v
      }
      state.RemoteVars = varsCopy
      return state
  }
- Do not expose internal mutable slices/maps directly. If an API must iterate over a collection that is guarded by a lock, provide a locked copy for iteration (avoid iterating over the locked map). Use helper methods like remote.GetRemoteMap() that return a copy.
- Protect read-modify-write operations (e.g., append/offset updates) with a lock or an atomic protocol. If an operation must be atomic across multiple fields, hold the mutex for the entire operation.
- Use reference counting or equivalent coordination when cache entries or resources may be concurrently flushed and used. Only remove/zero resources when ref count is zero and hold the lock while updating refs.
- Make channel ownership explicit: only the sender should close a channel. Do not attempt to close a channel from a receiver. If draining with a timeout, avoid hiding ownership errors—fail fast or document panic behavior deliberately.
- Prefer fail-fast when unexpected contention indicates a logic error (e.g., file-create flock): return an error immediately rather than silently waiting.
- Choose callbacks vs channels deliberately: callbacks are lightweight and can capture closures but will run inline and block the caller; channels can decouple execution and allow concurrency but add complexity. Document blocking behavior and ensure caller expectations are clear.

Why: these rules address several recurring concurrency bugs in our codebase—races caused by sharing internal state (maps/slices), races when updating file offsets or cache entries concurrently, unsafe iteration over maps, incorrect channel closing, and hidden blocking. Applying them reduces data races, unexpected panics, and subtle bugs during marshaling or concurrent operations.

Quick patterns:
- Safe accessor that returns snapshot: provide function that locks, copies, unlocks, return copy.
- Refcount pattern for cache entry:
  entry.Lock.Lock()
  entry.Refs++
  entry.Lock.Unlock()
  // use entry
  entry.Lock.Lock()
  entry.Refs--
  if entry.Refs == 0 && shouldRemove { remove }
  entry.Lock.Unlock()

References: [0,1,2,3,4,5,6,7]