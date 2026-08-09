---
title: Meaningful, Test-Level Correctness
description: 'Tests should be aligned with what they claim to validate, and placed
  at the right layer (unit vs integration). Concretely:


  - **Don’t rely on system side effects in unit tests.** If the test depends on vmnet/network/kernel/fs
  behavior, prefer **integration** coverage; unit tests should focus on pure logic.'
repository: apple/container
label: Testing
language: Swift
comments_count: 13
repository_stars: 48787
---

Tests should be aligned with what they claim to validate, and placed at the right layer (unit vs integration). Concretely:

- **Don’t rely on system side effects in unit tests.** If the test depends on vmnet/network/kernel/fs behavior, prefer **integration** coverage; unit tests should focus on pure logic.
- **Validate the real observable behavior.** Avoid indirect checks that can miss regressions (e.g., a kernel-set test should confirm the running kernel via `uname -r`, not just that the command succeeded). For CLI/progress rendering, assert the **actual emitted bytes** (use a `Pipe`, read raw output, check `\n` vs `\r`, and ensure no extra lines).
- **Make assertions match the intended semantics.** Remove “weird” expectations and assert the specific resources that should change (e.g., prune should delete the volumes you created).
- **Add boundary/edge-case coverage for pure logic.** If a rule exists (like max container name length), add unit tests for the exact boundary.
- **Improve robustness for filesystem/cleanup behavior.** Use deterministic allocation (e.g., prefer `/dev/urandom`), add `sync` before/after, and assert on measurable effects rather than assuming timing.

Example pattern for meaningful terminal assertions:
```swift
func testPlainModeTerminalOutput() async throws {
    let pipe = Pipe()
    let config = try ProgressConfig(
        terminal: pipe.fileHandleForWriting,
        description: "Task",
        outputMode: .plain
    )
    let progress = ProgressBar(config: config)
    progress.render(force: true)
    progress.finish()
    try pipe.fileHandleForWriting.close()

    let data = pipe.fileHandleForReading.readDataToEndOfFile()
    let output = String(decoding: data, as: UTF8.self)
    #expect(output.components(separatedBy: "\n").count == 3) // exactly two lines
}
```

Apply the same idea to other “claim vs reality” gaps: if the test name implies a behavior, the assertions must directly observe it.