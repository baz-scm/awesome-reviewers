---
title: prefer modern composition patterns
description: Use Vue 3 Composition API patterns that provide better performance, type
  safety, and maintainability. Prefer `computed` over `watch` + reactive assignment
  when deriving values from other reactive data. Use `defineEmits` instead of `$emit`
  in templates for type safety. Adopt modern `defineProps<{}>()` syntax over PropType
  casting for better TypeScript...
repository: cypress-io/cypress
label: Vue
language: Other
comments_count: 5
repository_stars: 48850
---

Use Vue 3 Composition API patterns that provide better performance, type safety, and maintainability. Prefer `computed` over `watch` + reactive assignment when deriving values from other reactive data. Use `defineEmits` instead of `$emit` in templates for type safety. Adopt modern `defineProps<{}>()` syntax over PropType casting for better TypeScript inference and performance. Consider `watchEffect` when you need `watch` with `immediate: true`.

Examples:
```ts
// ❌ Avoid watch + assignment pattern
const promptToShow = ref('')
watch(savedState, (newVal) => {
  promptToShow.value = computePrompt(newVal)
})

// ✅ Use computed for derived values
const promptToShow = computed(() => {
  return computePrompt(savedState.value)
})

// ❌ Avoid $emit in templates
@click="$emit('removeProject', props.gql.projectRoot)"

// ✅ Use defineEmits for type safety
const emit = defineEmits<{
  (e: 'removeProject', path: string): void
}>()
@click="emit('removeProject', props.gql.projectRoot)"

// ❌ Avoid PropType casting
const props = defineProps({
  gql: {
    type: Object as PropType<PackagesListFragment>,
    required: true
  }
})

// ✅ Use generic syntax for better inference
const props = defineProps<{
  gql: PackagesListFragment
}>()

// ✅ Use watchEffect for immediate watching
watchEffect(() => {
  docsMenuVariant.value = props.forceOpenDocs ? 'ci1' : 'main'
})
```

These patterns reduce boilerplate, improve TypeScript performance in IDEs, provide better type safety, and align with Vue 3 best practices.