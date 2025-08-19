---
title: RESTful endpoint organization
description: API endpoints should be properly organized around resources and follow
  RESTful principles. Avoid placing aggregation or utility endpoints in viewsets where
  they don't belong conceptually.
repository: PostHog/posthog
label: API
language: Python
comments_count: 4
repository_stars: 28460
---

API endpoints should be properly organized around resources and follow RESTful principles. Avoid placing aggregation or utility endpoints in viewsets where they don't belong conceptually.

Each viewset should represent a specific resource type, and endpoints within that viewset should operate on that resource. When you need aggregation endpoints or cross-resource operations, create dedicated API endpoints rather than forcing them into existing viewsets.

Example of what to avoid:
```python
# DON'T: Adding aggregation endpoint to external_data_source viewset
class ExternalDataSourceViewSet(ModelViewSet):
    @action(methods=["GET"], detail=False)
    def dwh_scene_stats(self, request):  # This doesn't belong here
        # Returns aggregated data warehouse statistics
        pass
```

Example of proper organization:
```python
# DO: Create dedicated endpoint for aggregations
class DataWarehouseViewSet(ModelViewSet):
    @action(methods=["GET"], detail=False) 
    def scene_stats(self, request):
        # Returns aggregated data warehouse statistics
        pass
```

For individual vs collection resources, handle both cases properly:
```python
# Handle both individual survey and survey collection
def surveys(request: Request):
    if survey_id:
        # Return individual survey with proper error handling
        try:
            survey = Survey.objects.get(id=survey_id, team=team)
            return JsonResponse({"survey": serialized_survey})
        except Survey.DoesNotExist:
            return JsonResponse({"error": "Survey not found"}, status=404)
    
    # Return collection of surveys
    return JsonResponse(get_surveys_response(team))
```

This approach makes APIs more intuitive, maintainable, and follows REST conventions that frontend developers expect.