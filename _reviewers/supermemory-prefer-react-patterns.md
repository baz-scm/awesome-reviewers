---
title: Prefer React Patterns
description: Write React components so state and events are handled using standard
  React patterns (hooks/state setters correctly, pending/loading comes from React/Form
  hooks, and key events don’t accidentally trigger default browser behavior). Also,
  pick the right navigation strategy when component-scoped data must be reset.
repository: supermemoryai/supermemory
label: React
language: TSX
comments_count: 4
repository_stars: 28844
---

Write React components so state and events are handled using standard React patterns (hooks/state setters correctly, pending/loading comes from React/Form hooks, and key events don’t accidentally trigger default browser behavior). Also, pick the right navigation strategy when component-scoped data must be reset.

Practical rules:
1) Use hook-provided pending/loading state
- Avoid duplicating setLoading(true/false) across handlers when your UI already supports pending state.

2) Always prevent default for “submit-like” Enter behavior in text inputs/content-editables
- If Enter shouldn’t create a newline, call e.preventDefault() before invoking your send action.

3) Prefer useReducer for “force re-render” triggers
- For simulation tick updates that need re-rendering, use a reducer increment pattern.

4) Use soft routing when you can, but hard reload when you must reset scoped caches/state
- If your next route depends on clearing org-scoped caches, prefer a full reload in that path.

Examples:

// 1) Pending state (avoid manual setLoading in many places)
function SubmitButton() {
  const { pending } = useFormStatus();
  return <button disabled={pending}>{pending ? 'Saving…' : 'Save'}</button>;
}

// 2) Prevent newline + send
onKeyDown={(e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    onSend();
  }
}}

// 3) Force render on simulation tick
const [, forceRender] = useReducer((x: number) => x + 1, 0);

useEffect(() => {
  if (!enabled) return;
  const sim = createSimulation();
  sim.on('tick', () => {
    onSimulationTick();
    forceRender();
  });
  return () => sim.stop();
}, [enabled, onSimulationTick]);

// 4) Route strategy: hard reload when you must reset scoped caches
// router.push(...) is fine for soft client transitions when prior caches don’t apply.
// If you must wipe org-scoped state, use a hard reload for that create-from-settings path.