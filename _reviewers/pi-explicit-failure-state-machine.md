---
title: Explicit failure state machine
description: 'When code has multi-step lifecycle operations (spawn/register/sync/stop)
  or user/config-driven behavior, make failures explicit and recoverable: model the
  lifecycle with a small state machine, track which resources were acquired so teardown
  can always run safely in reverse, and degrade gracefully with validated fallbacks
  and user-visible diagnostics. Also...'
repository: earendil-works/pi
label: Error Handling
language: TypeScript
comments_count: 3
repository_stars: 79783
---

When code has multi-step lifecycle operations (spawn/register/sync/stop) or user/config-driven behavior, make failures explicit and recoverable: model the lifecycle with a small state machine, track which resources were acquired so teardown can always run safely in reverse, and degrade gracefully with validated fallbacks and user-visible diagnostics. Also keep retry/error event schemas unambiguous so monitoring and recovery logic can reliably interpret what happened.

Apply it like this:
- Use states with an `error` state reachable from any step.
- Record acquired resources (e.g., `rpcProcess`, `sessionId`, `radiusId`) separately; on any failure, run best-effort cleanup in reverse acquisition order.
- For user-provided configs/themes: validate on load; if incomplete/invalid, switch to a safe default and warn with exactly what’s missing.
- For retries: ensure start/end (and any “attempt” metadata) are consistent—avoid having multiple events with overlapping meaning unless they convey distinct semantics.

Example (pattern):
```ts
type State = 'starting' | 'online' | 'stopping' | 'stopped' | 'error';

class RpcLifecycle {
  private state: State = 'stopped';
  private acquired: {
    rpcProcess?: { stop(): Promise<void> };
    sessionId?: string;
    radiusId?: string;
  } = {};

  async start() {
    this.state = 'starting';
    try {
      // 1) acquire resources step-by-step
      this.acquired.rpcProcess = await this.startRpc();
      this.acquired.sessionId = await this.syncSession();
      this.acquired.radiusId = await this.registerRadius();

      this.state = 'online';
    } catch (e) {
      await this.cleanupBestEffort();
      this.state = 'error';
      throw e;
    }
  }

  private async cleanupBestEffort() {
    // reverse order of acquisition
    if (this.acquired.radiusId) await this.unregisterRadiusBestEffort(this.acquired.radiusId);
    if (this.acquired.sessionId) await this.unsyncSessionBestEffort(this.acquired.sessionId);
    if (this.acquired.rpcProcess) await this.acquired.rpcProcess.stop().catch(() => {});

    this.acquired = {};
  }
}
```