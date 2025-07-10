---
title: Use proper logging
description: Always use the project's standard logging system (mbgl::Log) with appropriate
  log levels instead of ad-hoc solutions like std::cout, printf, or custom logging
  macros. This ensures consistent log formatting, proper filtering, and integration
  with test frameworks.
repository: maplibre/maplibre-native
label: Logging
language: C++
comments_count: 4
repository_stars: 1411
---

Always use the project's standard logging system (mbgl::Log) with appropriate log levels instead of ad-hoc solutions like std::cout, printf, or custom logging macros. This ensures consistent log formatting, proper filtering, and integration with test frameworks.

Key guidelines:
1. Use mbgl::Log with the appropriate event type and level:
   ```cpp
   // Instead of:
   // std::cout << "-------- HASTILE - FOUND IN TILES\n";
   // or:
   #if MLN_PLUGIN_LAYER_LOGGING_ENABLED
   std::cout << "Working on: " << name << "\n";
   #endif

   // Use:
   Log::Debug(Event::General, "HASTILE - FOUND IN TILES");
   // or for errors:
   Log::Error(Event::OpenGL, "Failed to open X display, retrying...");
   ```

2. Choose the correct log level based on message importance:
   - Debug: Detailed information useful during development
   - Info: General operational messages
   - Warning: Concerning but non-fatal issues
   - Error: Serious problems that need attention

3. Add logging for error conditions and edge cases to improve visibility:
   ```cpp
   if (!checkAndSetMode(Mode::Primitives)) {
       Log::Warning(Event::Render, "Cannot add triangle with current mode");
       return;
   }
   ```

4. Remove commented-out debug prints from production code or convert them to proper logging calls.

Be mindful that log levels can affect test behavior - some test fixtures may filter specific log levels.