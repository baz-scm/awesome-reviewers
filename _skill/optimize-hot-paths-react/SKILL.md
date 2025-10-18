---
name: optimize-hot-paths-react
description: "Reduce unnecessary operations in performance-critical React code paths to improve runtime speed."
---

# Optimize Hot Paths (React)

In performance-critical code that runs frequently (e.g. rendering loops or event handlers), minimize any work that isn’t absolutely needed[1]. Key guidelines include:

- **Cache repeated computations.** Avoid redundant calculations (like repeated `typeof` checks or expensive function calls inside loops). Compute once, store the result, and reuse it[2][3].
- **Avoid unnecessary allocations.** Reuse data structures instead of creating new arrays/objects in hot code. Every allocation has a cost; prefer in-place operations when possible[2].
- **Traverse directly.** When iterating over DOM nodes or data structures, operate directly on the collection rather than building intermediate lists. For example, add event listeners in one pass over elements instead of constructing a new array or `Set` of those elements[4].
- **Mind execution thresholds.** Be aware of how fast operations need to be. Aim for `<1ms` operations in ultra-hot loops, `<10ms` for per-frame work (to maintain 60fps), and `<100ms` for interactions[5]. If an operation exceeds these thresholds in a hot path, refactor or optimize it.

By aggressively optimizing these hot paths, we prevent minor inefficiencies from scaling into major slowdowns. This results in a snappier UI and smoother React application performance under load[5].
