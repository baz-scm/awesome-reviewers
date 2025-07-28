---
title: Semantic variable naming
description: 'Variable names should clearly convey their purpose, type, and units
  to improve code readability and prevent errors. Follow these naming conventions:


  **Unit specification**: Include units in variable names when dealing with measurements
  or time values. Use suffixes like `Us` for microseconds, `Ms` for milliseconds,
  etc.'
repository: hyprwm/Hyprland
label: Naming Conventions
language: C++
comments_count: 4
repository_stars: 28863
---

Variable names should clearly convey their purpose, type, and units to improve code readability and prevent errors. Follow these naming conventions:

**Unit specification**: Include units in variable names when dealing with measurements or time values. Use suffixes like `Us` for microseconds, `Ms` for milliseconds, etc.
```cpp
// Bad
void renderData(CMonitor* pMonitor, float duration) {
    m_dLastRenderTimes.push_back(duration / 1000.f);
}

// Good  
void renderData(CMonitor* pMonitor, float durationUs) {
    m_dLastRenderTimes.push_back(durationUs / 1000.f);
}
```

**Intuitive naming**: Choose names that clearly express intent and behavior. Prefer descriptive names over abbreviated ones.
```cpp
// Bad
m_pConfig->addConfigValue("binds:pin_fullscreen", Hyprlang::INT{0});

// Good
m_pConfig->addConfigValue("binds:allow_pin_fullscreen", Hyprlang::INT{0});
```

**Pointer prefixes**: Use `p` prefix only for actual pointer variables, not for other types.
```cpp
// Bad
const auto pwindowCurrentFullscreenState = PWINDOW->m_bIsFullscreen;
const auto pwindowCurrentFullscreenMode = PWINDOW->m_pWorkspace->m_efFullscreenMode;

// Good
const auto CURRENTWINDOWFSSTATE = PWINDOW->m_bIsFullscreen;
const auto CURRENTWINDOWFSMODE = PWINDOW->m_pWorkspace->m_efFullscreenMode;
```

**Case conventions**: Use camelCase for variables and function names, CAPS for constants. Avoid snake_case.
```cpp
// Bad
const auto target_portion = (*PGAPSOUT + *PBORDERSIZE) / (VERTANIMS ? PMONITOR->vecSize.y : PMONITOR->vecSize.x);
size_t space_pos = VALUE.find(' ');

// Good
const auto TARGETPORTION = (*PGAPSOUT + *PBORDERSIZE) / (VERTANIMS ? PMONITOR->vecSize.y : PMONITOR->vecSize.x);
size_t spacePos = VALUE.find(' ');
```

These conventions reduce cognitive load, prevent type-related bugs, and make code self-documenting.