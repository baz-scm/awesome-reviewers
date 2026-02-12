---
title: Centralize constants and structure
description: 'Motivation

  Keep code readable, consistent and easy to change by centralizing configuration,
  constants and mutable state, and by extracting repeated flows into well-scoped helpers
  or service types.'
repository: wavetermdev/waveterm
label: Code Style
language: Go
comments_count: 5
repository_stars: 17328
---

Motivation
Keep code readable, consistent and easy to change by centralizing configuration, constants and mutable state, and by extracting repeated flows into well-scoped helpers or service types.

Rules
- Move literal paths and long user-facing strings to package-level consts in the appropriate package (e.g., base or config). Don’t inline repeated strings. Example:
  // in base.go
  const ConfigDir = "config"
  const AIUseTelemetryMsg = `In order to protect against abuse, you must have telemetry turned on ...`
  // usage
  fullPath := path.Join(scbase.GetWaveHomeDir(), ConfigDir, filePath)

- Replace package-level mutable globals with concrete types that implement interfaces. This enables multiple instances, easier testing, and clearer ownership of state. Example:
  // instead of package globals:
  // var cache map[string]*CacheEntry

  type BlockStoreType struct {
    mu    sync.Mutex
    cache map[string]*CacheEntry
    // other fields
  }

  func NewBlockStore() *BlockStoreType { return &BlockStoreType{cache: map[string]*CacheEntry{}} }

  // implement BlockStore methods on *BlockStoreType

- Remove boilerplate by extracting common flows into helpers or central services. If multiple code paths perform the same multi-step operation (e.g., copying files between remotes and writing to PTY), consolidate into a single function or route through a central component (mshell). This reduces duplicate writeStringToPty calls and branching.
  Example:
  // high-level helper
  func copyFileRemoteToRemote(ctx context.Context, src RemoteRef, dst RemoteRef, opts CopyOpts) error { /* unified logic */ }

  // caller becomes a small orchestration wrapper
  err := copyFileRemoteToRemote(ctx, sourceRemoteId, destRemoteId, opts)

- Prefer idiomatic, simple APIs when building payloads or encoding. For JSON request payloads, use json.Marshal to get []byte directly instead of manual bytes.Buffer + Encoder when appropriate:
  payload, err := json.Marshal(cloudCompletionRequestConfig)
  if err != nil { return err }
  req, _ := http.NewRequest("POST", url, bytes.NewReader(payload))

Application guidance
- Put constants in logical packages (base/config for paths, a strings or msgs package for long messages if reused across files).
- When you spot repeated sequences of statements (logging + pty writes + connection attempts), factor them into a single helper and add tests for that helper.
- When a package uses mutable shared state, prefer wrapping it in a type with methods and constructors (NewX) and keep package-level variables minimal.
- Small, local refactors that centralize behavior are preferred over ad-hoc fixes scattered across files.

Why this matters
Centralizing constants and state improves discoverability and reduces risk when changing behavior (e.g., renaming the config directory or changing a long message). Extracting repeated logic reduces bugs and makes reasoning/test coverage easier. Using idiomatic APIs keeps code concise and consistent.

References: 0,1,2,3,4