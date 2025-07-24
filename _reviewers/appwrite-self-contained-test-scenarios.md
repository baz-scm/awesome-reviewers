---
title: Self-contained test scenarios
description: 'Tests should be fully self-contained to ensure reliability and prevent
  unexpected failures. Each test scenario should:


  1. Create any prerequisite data it needs rather than assuming it exists'
repository: appwrite/appwrite
label: Testing
language: Other
comments_count: 3
repository_stars: 51959
---

Tests should be fully self-contained to ensure reliability and prevent unexpected failures. Each test scenario should:

1. Create any prerequisite data it needs rather than assuming it exists
2. Explicitly clean up data after test execution
3. Avoid dependencies on other test scenarios
4. Use parameterized values instead of hardcoded data

**Benefits:**
- Tests can run independently and in any order
- Test suites are more reliable and less prone to cascading failures
- Test maintenance becomes simpler when individual tests are isolated

**Example - Before:**
```gherkin
Escenario: Como administrador, puedo renombrar un proyecto existente
  Dado que la API está disponible
  Y dado que existe un proyecto "ProyectoPrueba" con ID $projectId
  Cuando el Actor envía PATCH /v1/projects/$projectId con:
    | name | "ProyectoRenombrado" |
  Entonces el código de respuesta debe ser 200
```

**Example - After:**
```gherkin
Escenario: Como administrador, puedo renombrar un proyecto existente
  Dado que la API está disponible
  Y que creo un proyecto "ProyectoPrueba" y guardo su ID como $projectId
  Cuando el Actor envía PATCH /v1/projects/$projectId con:
    | name | "ProyectoRenombrado" |
  Entonces el código de respuesta debe ser 200
  Y el JSON retornado debe tener name "ProyectoRenombrado"
  Y limpio el proyecto creado
```