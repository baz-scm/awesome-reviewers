---
title: Modern React Mounting
description: 'When building React components that wrap external resources (e.g., WebGL/canvas),
  follow these rules:


  - Forward refs for React 18+ compatibility: use `forwardRef` rather than custom
  ref plumbing.'
repository: paper-design/shaders
label: React
language: TSX
comments_count: 4
repository_stars: 3286
---

When building React components that wrap external resources (e.g., WebGL/canvas), follow these rules:

- Forward refs for React 18+ compatibility: use `forwardRef` rather than custom ref plumbing.
- Never call hooks conditionally: all `useState/useEffect/useLayoutEffect/useRef` must be unconditional.
- Make async initialization/update effects race-safe: cancel/guard async work, and dispose the external resource on unmount.
- Use React-compatible types: prefer `React.ReactElement` over `JSX.Element` in newer React type setups.

Example pattern:
```tsx
export const ShaderMount = forwardRef<HTMLCanvasElement, Props>(function ShaderMountImpl(
  { fragmentShader, uniforms, speed = 1, frame = 0 },
  forwardedRef
) {
  const canvasRef = typeof forwardedRef === 'function'
    ? forwardedRef // handle callback refs externally by not assuming .current
    : (forwardedRef ?? useRef<HTMLCanvasElement>(null));

  const [mount, setMount] = useState<ShaderMountVanilla | null>(null);

  useLayoutEffect(() => {
    const canvas = (canvasRef as React.RefObject<HTMLCanvasElement> | null)?.current;
    if (!canvas || mount) return;

    let cancelled = false;
    processUniforms(uniforms).then((u) => {
      if (cancelled || !canvas) return;
      setMount(new ShaderMountVanilla(canvas, fragmentShader, u, /* attrs */ speed, frame));
    });

    return () => {
      cancelled = true;
      mount?.dispose();
    };
  }, [fragmentShader, uniforms, mount, speed, frame]);

  return <canvas ref={canvasRef as any} />;
});
```

Apply this to ensure ref correctness across React versions, prevent hook/ref breakage, and avoid subtle lifecycle/race issues with async WebGL setup and uniform updates.