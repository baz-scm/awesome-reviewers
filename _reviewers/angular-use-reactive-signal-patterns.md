---
title: Use reactive signal patterns
description: Prefer Angular's reactive signal patterns over manual subscription management
  and imperative approaches. Use signals directly in templates without calling getters,
  convert observables to signals with `toSignal()`, and maintain reactive data flow
  throughout your application.
repository: angular/angular
label: Angular
language: Markdown
comments_count: 6
repository_stars: 98611
---

Prefer Angular's reactive signal patterns over manual subscription management and imperative approaches. Use signals directly in templates without calling getters, convert observables to signals with `toSignal()`, and maintain reactive data flow throughout your application.

Key practices:
- In templates, reference signals directly: `[(checked)]="mySignal"` not `[(checked)]="mySignal()"`
- Convert observables to signals with `toSignal()` for reactive data that updates over time
- Use `toSignal(router.events.pipe(map(() => !!router.getCurrentNavigation())))` instead of manual subscription management for navigation state
- Avoid creating unnecessary signals just to trigger effects - work directly with observables when appropriate

Example of preferred reactive pattern:
```ts
@Component({
  template: `
    @if (loading()) {
      <div>Loading...</div>
    }
    <div [class.admin]="isAdmin" [class.dense]="density() === 'high'">
  `
})
export class MyComponent {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  
  // Convert observable to signal for reactive updates
  private data = toSignal(this.route.data);
  user = computed(() => this.data()?.user as User);
  
  // Use toSignal for navigation state
  loading = toSignal(
    this.router.events.pipe(
      map(() => !!this.router.getCurrentNavigation())
    ),
    { initialValue: false }
  );
  
  // Direct signal usage in two-way binding
  isAdmin = signal(false);
  density = signal<'normal' | 'high'>('normal');
}
```

This approach provides better performance, cleaner code, and leverages Angular's reactive primitives effectively.