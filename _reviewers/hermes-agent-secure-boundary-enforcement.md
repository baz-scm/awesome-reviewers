---
title: Secure boundary enforcement
description: When code crosses security boundaries (HTTP auth, subprocess execution,
  or policy-driven external side effects), it must follow the established secure path
  and validate before acting.
repository: nousresearch/hermes-agent
label: Security
language: JavaScript
comments_count: 3
repository_stars: 221948
---

When code crosses security boundaries (HTTP auth, subprocess execution, or policy-driven external side effects), it must follow the established secure path and validate before acting.

- **Use the project’s authenticated transport**: Don’t bypass SDK helpers with ad-hoc `fetch`/manual token headers. Forward extra headers (e.g., locale) via the helper’s options so cookie-based/OAuth flows remain intact.
  
  ```js
  // Prefer the SDK helper that preserves cookie/OAuth behavior
  return SDK.fetchJSON(url, {
    method: 'GET',
    headers: {
      ...(locale && locale !== 'en' ? { 'Accept-Language': locale } : {}),
      // do not manually inject window tokens if the SDK already handles auth
    },
  });
  ```

- **Prevent command injection**: Never build a shell command string from untrusted inputs. Use argument-vector subprocess APIs.

  ```js
  // Unsafe (shell string composition): avoid
  // execSync(`ffmpeg -i "${file}" ...`)

  // Safe: argument array
  execFileSync('ffmpeg', ['-i', filePath, /* ... */], { stdio: 'inherit' });
  ```

- **Gate privileged side effects**: Validate authorization/policy and required identifiers *before* queueing or emitting actions. Only collect/execute the side effect after admission checks pass.

  ```js
  const queued = [];
  for (const msg of messages) {
    if (!msg.key || msg.key.fromMe) continue;
    const chatId = msg.key.remoteJid;
    if (!chatId || chatId.endsWith('@broadcast') || chatId.endsWith('@g.us')) continue;

    // enqueue only after policy gates/allowlists have been applied
    if (passesAdmissionChecks(msg)) queued.push(msg.key);
  }
  ```

Apply these rules consistently to reduce auth regressions (401/OAuth gating), injection risk, and inadvertent disclosure/side effects from policy mistakes.