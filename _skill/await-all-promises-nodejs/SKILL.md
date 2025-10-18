---
name: await-all-promises-nodejs
description: "Always await asynchronous operations in Node.js (especially in cleanup or shutdown code) to avoid race conditions and resource leaks."
---

# Await All Promises (Node.js)

Node.js applications are heavily asynchronous. A common source of bugs is not waiting for promises to settle before continuing, which can lead to race conditions and leaked resources[26]. This skill instructs reviewers to always check for proper `await` usage:

- **Await every async operation.** If a function returns a `Promise`, ensure the code either awaits it or handles it with `.then()`/`.catch()`. This is particularly important in cleanup logic (closing files, connections) or sequential tasks. For example, if an option says `autoClose`, calling `this.close()` without `await` might not close the resource before the next operation begins. The correct approach is `if (options.autoClose) await this.close();` to fully close the resource before proceeding[27].
- **Use modern patterns for clarity.** Encourage the use of utility patterns like `Promise.withResolvers()` or `util.promisify` to handle asynchronous flows instead of older callback styles[28]. This makes code easier to await and less error-prone.
- **Preserve async context.** In complex Node apps, ensure that asynchronous context (like continuation-local storage via `AsyncLocalStorage`) is not broken. When using APIs that accept callbacks, wrap them so that context is maintained (for instance, using `als.run()` and careful usage of async functions inside callbacks)[29].

By systematically awaiting promises, we prevent situations where Node would continue execution before an operation completes. This leads to more reliable concurrency, no orphaned operations, and clean shutdown sequences (e.g., no DB transactions left hanging because the process exited early)[26].
