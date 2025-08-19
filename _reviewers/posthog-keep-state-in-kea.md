---
title: Keep state in Kea
description: React components should focus on presentation and user interaction, not
  state management logic. All state logic should be contained within Kea stores, with
  components only pulling in actions and values. This separation improves testability,
  reusability, and maintainability.
repository: PostHog/posthog
label: React
language: TSX
comments_count: 2
repository_stars: 28460
---

React components should focus on presentation and user interaction, not state management logic. All state logic should be contained within Kea stores, with components only pulling in actions and values. This separation improves testability, reusability, and maintainability.

Components should avoid:
- useState and useEffect for business logic
- Complex state calculations
- Direct API calls or data fetching

Instead, delegate these responsibilities to Kea logic files and consume the results:

```tsx
// ❌ Avoid: State logic in component
export function DataWarehouseScene(): JSX.Element {
    const [recentActivity, setRecentActivity] = useState<UnifiedRecentActivity[]>([])
    const [totalRowsProcessed, setTotalRowsProcessed] = useState<number>(0)
    
    useEffect(() => {
        const loadData = async (): Promise<void> => {
            const [activities, totalRows] = await Promise.all([
                fetchRecentActivity(dataWarehouseSources?.results || [], materializedViews),
                fetchTotalRowsProcessed(dataWarehouseSources?.results || [], materializedViews),
            ])
            setRecentActivity(activities)
            setTotalRowsProcessed(totalRows)
        }
        loadData()
    }, [dataWarehouseSources?.results, materializedViews])
}

// ✅ Preferred: State logic in Kea, component consumes values
export function DataWarehouseScene(): JSX.Element {
    const { recentActivity, totalRowsProcessed } = useValues(dataWarehouseLogic)
    const { loadDashboardData } = useActions(dataWarehouseLogic)
}
```

This pattern ensures components remain focused on rendering and user interactions while keeping business logic centralized and testable.