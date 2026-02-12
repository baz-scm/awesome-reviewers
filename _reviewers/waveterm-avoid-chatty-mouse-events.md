---
title: Avoid chatty mouse events
description: 'Motivation: High-frequency events like mousemove are "chatty" and can
  cause excessive CPU usage and layout thrashing. Prefer lower-rate pointer events
  (mouseenter/mouseleave) or throttled handlers attached to specific elements, and
  minimize repeated DOM writes by toggling classes. Always attach and remove listeners
  in lifecycle hooks and guard against null...'
repository: wavetermdev/waveterm
label: Performance Optimization
language: TSX
comments_count: 2
repository_stars: 17328
---

Motivation: High-frequency events like mousemove are "chatty" and can cause excessive CPU usage and layout thrashing. Prefer lower-rate pointer events (mouseenter/mouseleave) or throttled handlers attached to specific elements, and minimize repeated DOM writes by toggling classes. Always attach and remove listeners in lifecycle hooks and guard against null refs to avoid leaks.

How to apply:
- Replace document-level or continuous mousemove handlers with a lightweight hover hotspot (e.g., a full-width fixed div) that uses mouseenter to reveal UI and mouseleave on the revealed element to hide it.
- Toggle CSS classes rather than repeatedly writing inline styles to reduce layout and paint costs.
- Use useEffect (or equivalent) to add/remove event listeners and to read element sizes once, guarding ref nulls.
- If you must track movement, throttle/debounce the handler and limit work done per call.

Example (pattern adapted from the discussion):

// setup
const autoHideTabBar = settings?.["window:autohidetabbar"] ?? false;

useEffect(() => {
  const tabBar = tabbarWrapperRef.current;
  if (!tabBar) return;

  if (!autoHideTabBar) {
    tabBar.style.top = '0px';
    return;
  }

  const tabBarHeight = tabBar.clientHeight + 1;
  tabBar.style.top = `-${tabBarHeight - 10}px`;

  const onEnter = () => {
    // show via class toggle to avoid many inline writes
    tabBar.classList.add('tab-bar-wrapper-auto-hide-visible');
    tabBar.style.top = '0px';
    tabBar.addEventListener('mouseleave', onLeave);
  };

  const onLeave = () => {
    tabBar.classList.remove('tab-bar-wrapper-auto-hide-visible');
    tabBar.style.top = `-${tabBarHeight - 10}px`;
    tabBar.removeEventListener('mouseleave', onLeave);
  };

  // attach to the hotspot element (not document) to avoid global mouse tracking
  tabbarWrapperRef.current.addEventListener('mouseenter', onEnter);
  return () => {
    tabbarWrapperRef.current?.removeEventListener('mouseenter', onEnter);
    tabbarWrapperRef.current?.removeEventListener('mouseleave', onLeave);
  };
}, [autoHideTabBar]);

Notes:
- Guard ref accesses (tabbarWrapperRef.current) to prevent runtime errors.
- Prefer class toggles for visibility so CSS handles transitions and reduces JS-driven layout changes.
- If you need finer-grained movement tracking, apply throttling and keep DOM reads/writes batched.