---
title: Atomic Concurrency Contracts
description: 'All concurrency-sensitive code must follow an “atomic + lifecycle-valid”
  contract.


  **Rules**

  1. **Make check-then-act atomic.** If you verify a precondition and then mutate
  shared state (e.g., “volume not in use => delete”), do both while holding the same
  synchronization boundary (actor/lock). Prefer closure-based helpers that keep the
  lock for the whole...'
repository: apple/container
label: Concurrency
language: Swift
comments_count: 8
repository_stars: 48787
---

All concurrency-sensitive code must follow an “atomic + lifecycle-valid” contract.

**Rules**
1. **Make check-then-act atomic.** If you verify a precondition and then mutate shared state (e.g., “volume not in use => delete”), do both while holding the same synchronization boundary (actor/lock). Prefer closure-based helpers that keep the lock for the whole check+mutation.
2. **Capture decisions under the lock.** If later operations depend on a value that may change (e.g., flags/options determined while the container still exists), compute/store it while locked and use the stored value outside the lock.
3. **Validate lifecycle immediately before async continuation.** Async completions (connect callbacks, background tasks) must not call into code paths after teardown/removal. Either (a) guard via “is still active”/state under the proper context, or (b) use a synchronization mechanism that makes completion observe the latest lifecycle state.
4. **Prevent blocking I/O deadlocks.** For tests and IPC involving blocking pipes/FIFOs or child stdout/stderr, ensure producers/consumers are connected concurrently and/or redirect/drain output so the child can’t block.
5. **Use actor isolation or a single state mutex.** Don’t mix partial mutexing with actor isolation in ways that leave invariants unclear; avoid `nonisolated(unsafe)` unless you can prove all accesses are synchronized.

**Illustrative patterns**

*Atomic delete check (closure holds lock during check+delete):*
```swift
try await volumesService.delete(name: volume) // implementation should do:
try await containersService.withContainerList { containers in
  guard !containers.contains(where: { $0.isUsingVolume(volume) && $0.isRunning() }) else {
    throw VolumeError.volumeInUse(volume)
  }
  try await volumeStore.delete(volume)
}
```

*Teardown-safe async completion (guard active state before acting):*
```swift
.whenComplete { result in
  switch result {
  case .success(let channel):
    guard context.channel.isActive else {
      channel.close(promise: nil)
      return
    }
    self.glue(channel, context: context)
  case .failure(let error):
    context.close(promise: nil)
    context.fireErrorCaught(error)
  }
}
```

*Deadlock-free FIFO test (writer+reader concurrently):*
```swift
let group = DispatchGroup()
group.enter()
DispatchQueue.global().async {
  defer { group.leave() }
  let handle = try! FileHandle(forWritingTo: pipePath)
  try! handle.write(contentsOf: "SECRET_KEY=value123\n".data(using: .utf8)!)
  try! handle.close()
}
let lines = try Parser.envFile(path: pipePath)
group.wait()
```