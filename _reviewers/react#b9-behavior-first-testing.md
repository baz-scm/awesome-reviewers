---
title: Behavior-first testing
description: Prefer black-box tests that validate observable behavior end-to-end,
  driven by realistic interactions and asserted via stable public seams—rather than
  unit-style checks of internal ordering/state or mocked “operation sequences”.
repository: facebook/react#b9
label: Testing
language: JavaScript
comments_count: 10
repository_stars: 251891
---

Prefer black-box tests that validate observable behavior end-to-end, driven by realistic interactions and asserted via stable public seams—rather than unit-style checks of internal ordering/state or mocked “operation sequences”.

Apply it like this:
- Drive user-like flows from the test using `act(...)` (and appropriate microtask/renderer flushing), not by embedding interaction orchestration inside the component.
- Observe real outputs (DOM changes, public events, backend-emitted events) that correspond to the behavior you’re fixing; don’t lean on internal implementation seams unless there’s no better observable.
- Keep assertions readable and robust: assert expected state *before* you switch modes, use fresh DOM/instance references per phase, and avoid comments that encode React implementation details as test requirements.
- Prefer consistent Jest patterns (`jest.spyOn`, standard matchers) over ad-hoc event log plumbing when you’re asserting side effects.

Example pattern (interaction driven from test):
```js
const submitBtnRef = React.createRef();
let bumpRender;

function App() {
  bumpRender = () => Scheduler.unstable_log('Render');
  return <form><button ref={submitBtnRef}>Submit</button></form>;
}

await actAsync(async () => {
  render(<App />);
  await waitFor(['Render']);
  submitBtnRef.current.click();
  await waitFor(['Render']);
  submitBtnRef.current.click();
});
```

If you can’t assert via public behavior, treat mocking/intercepting internals as a last resort and document why no stable observable seam exists.