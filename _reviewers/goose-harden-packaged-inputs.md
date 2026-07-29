---
title: Harden Packaged Inputs
description: 'Apply a production/packaged hardening rule: in release builds, only
  use trusted origins and trusted code/resources. Treat environment variables, URLs,
  and “implicit” host paths as untrusted inputs, and explicitly gate/validate them
  so they cannot redirect critical behavior.'
repository: aaif-goose/goose
label: Security
language: TypeScript
comments_count: 2
repository_stars: 51876
---

Apply a production/packaged hardening rule: in release builds, only use trusted origins and trusted code/resources. Treat environment variables, URLs, and “implicit” host paths as untrusted inputs, and explicitly gate/validate them so they cannot redirect critical behavior.

How to apply:
- Stable origin hosting: avoid `file://`/null-origin behaviors in packaged UI; ensure packaged assets are served from a deterministic scheme/origin via a controlled protocol handler.
- Trusted executable resolution: validate the path to binaries/resources; in packaged builds, ignore or explicitly reject environment-based overrides that could point to an attacker-controlled executable.
- Gate on mode: allow flexibility in dev/test, but tighten behavior when `isPackaged` (or equivalent release flag) is true.

Example pattern (combined):

```ts
// 1) Stable, non-file origin for packaged renderer
let packagedProtocolRegistered = false;
function registerPackagedRendererProtocol() {
  if (MAIN_WINDOW_VITE_DEV_SERVER_URL || packagedProtocolRegistered) return;
  session.fromPartition(GOOSE_SESSION_PARTITION).protocol.handle(
    PACKAGED_RENDERER_PROTOCOL,
    async (request) => {
      // Resolve to bundled resources only
      const resolved = resolvePackagedRendererPath(
        request.url,
        getPackagedRendererRoot()
      );
      if (!resolved) return new Response('Not found', { status: 404 });
      const data = await fs.readFile(resolved);
      return new Response(new Uint8Array(data), {
        headers: { 'Content-Type': rendererContentType(resolved) },
      });
    }
  );
  packagedProtocolRegistered = true;
}

function getAppUrl(): URL {
  if (MAIN_WINDOW_VITE_DEV_SERVER_URL) return new URL(MAIN_WINDOW_VITE_DEV_SERVER_URL);
  registerPackagedRendererProtocol();
  return packagedRendererUrl();
}

// 2) Reject env override in packaged builds
export function findGooseBinaryPath({ isPackaged, resourcesPath }: {
  isPackaged?: boolean;
  resourcesPath?: string;
} = {}): string {
  const envPath = process.env.GOOSE_BINARY;
  if (envPath) {
    if (isPackaged) {
      throw new Error('GOOSE_BINARY override is not allowed in packaged builds');
    }
    // dev/test: resolve & validate
    const resolved = path.resolve(envPath);
    if (existingFile(resolved)) return resolved;
    throw new Error('Invalid GOOSE_BINARY path');
  }

  // packaged: only use bundled resources
  const bundled = resourcesPath ? path.join(resourcesPath, 'bin', 'goose') : '';
  if (existingFile(bundled)) return bundled;
  throw new Error('Bundled goose binary not found');
}
```

Outcome: release behavior becomes deterministic and resistant to attacker-controlled origin or configuration inputs, reducing security risk while keeping dev/test ergonomics.