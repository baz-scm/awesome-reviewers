---
title: Assert behavior; inject inputs
description: When code changes affect what the app *sends* (RPC/HTTP payloads/options)
  or what the app *decides* based on the environment, add targeted tests that (1)
  assert the exact externally observable behavior and (2) make the inputs deterministic.
repository: nousresearch/hermes-agent
label: Testing
language: TypeScript
comments_count: 3
repository_stars: 221948
---

When code changes affect what the app *sends* (RPC/HTTP payloads/options) or what the app *decides* based on the environment, add targeted tests that (1) assert the exact externally observable behavior and (2) make the inputs deterministic.

Practical rules:
- Client/server contract: If a function changes a request field (e.g., RPC `session.create`), write a regression test that triggers the path (e.g., via the hook) and asserts the exact payload contains the new field/value.
- API wrapper options: If you add wrapper-level configuration (e.g., `timeoutMs`), add a focused unit test that calls the wrapper (or mounts the relevant layer) and asserts the options passed to the underlying API client.
- Environment detection: If logic depends on host/system files or runtime environment, refactor to inject the relevant values (like sysfs/DMI fields) so unit tests can deterministically cover QEMU/virtualization/non-match and read-failure branches.

Example (Vitest-style contract assertion):
```ts
import { describe, it, expect, vi } from 'vitest'
import { renderHook } from '@testing-library/react'
import { useSessionLifecycle } from './useSessionLifecycle'

vi.mock('../rpc', () => ({
  rpc: vi.fn(),
}))

it('sends launch cwd in session.create payload', async () => {
  process.env.HERMES_CWD = '/expected/launch/dir'

  const { rpc } = await import('../rpc')
  ;(rpc as unknown as ReturnType<typeof vi.fn>).mockResolvedValue({ /* ... */ })

  const { result } = renderHook(() =>
    useSessionLifecycle({ /* required opts */ })
  )

  await result.current.newSession(/* args that lead to startNewSession */)

  expect(rpc).toHaveBeenCalledWith('session.create', expect.objectContaining({
    cwd: '/expected/launch/dir',
  }))
})
```

Apply the same pattern to wrapper options (assert `timeoutMs`) and to environment detection (inject sysfs/DMI inputs rather than reading the host).