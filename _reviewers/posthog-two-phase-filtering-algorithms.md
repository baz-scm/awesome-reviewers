---
title: two-phase filtering algorithms
description: 'When working with large datasets or complex matching operations, implement
  algorithms that use a two-phase approach: first filter candidates using efficient
  broad criteria, then verify matches with precise logic. This pattern significantly
  improves performance by reducing the number of expensive operations.'
repository: PostHog/posthog
label: Algorithms
language: Python
comments_count: 2
repository_stars: 28460
---

When working with large datasets or complex matching operations, implement algorithms that use a two-phase approach: first filter candidates using efficient broad criteria, then verify matches with precise logic. This pattern significantly improves performance by reducing the number of expensive operations.

The approach is particularly effective when:
- Database-level filtering can eliminate most irrelevant records
- Verification logic is computationally expensive
- Memory usage needs to be minimized

Example implementation:
```python
def get_dependent_cohorts_reverse(cohort: Cohort) -> list[Cohort]:
    # Phase 1: Database-level filtering using broad criteria
    filter_conditions = Q()
    filter_conditions |= Q(filters__icontains=f'"value": {cohort.id}')
    filter_conditions |= Q(filters__icontains=f'"value": "{str(cohort.id)}"')
    
    candidate_cohorts = (
        Cohort.objects.filter(filter_conditions, team=cohort.team, deleted=False)
        .exclude(id=cohort.id)
    )
    
    dependent_cohorts = []
    
    # Phase 2: Precise verification of filtered candidates
    for candidate_cohort in candidate_cohorts:
        for prop in candidate_cohort.properties.flat:
            if prop.type == "cohort" and not isinstance(prop.value, list):
                try:
                    if int(prop.value) == cohort.id:
                        dependent_cohorts.append(candidate_cohort)
                        break
                except (ValueError, TypeError):
                    continue
    
    return dependent_cohorts
```

This pattern avoids loading all records into memory and performing expensive operations on irrelevant data, instead using the database's indexing and filtering capabilities first.