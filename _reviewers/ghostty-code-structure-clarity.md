---
title: Code structure clarity
description: Write code with clear structural organization that enhances readability
  and maintainability. Extract duplicated or complex logic into well-named functions,
  avoid deeply nested conditionals, and use proper type organization.
repository: ghostty-org/ghostty
label: Code Style
language: Other
comments_count: 9
repository_stars: 32864
---

Write code with clear structural organization that enhances readability and maintainability. Extract duplicated or complex logic into well-named functions, avoid deeply nested conditionals, and use proper type organization.

When identical code appears in multiple places, extract it to a function:
```zig
// Instead of repeating this code in multiple functions:
const count: usize = @intCast(self.nPages());
for (0..count) |position| {
    const page = self.tab_view.getNthPage(@intCast(position));
    // Complex logic here...
}

// Extract it to a dedicated function:
fn setPageIcons(self: *TabView) void {
    const count: usize = @intCast(self.nPages());
    for (0..count) |position| {
        const page = self.tab_view.getNthPage(@intCast(position));
        // Complex logic here...
    }
}
```

For nested conditionals, prefer block expressions or separate helper functions:
```zig
// Instead of deeply nested conditionals:
if (self.window.config.gtk_tab_icons) {
    if (position < 10) {
        // Logic here
    } else {
        // Other logic
    }
} else {
    // Yet another logic
}

// Use block expressions or early returns:
const icon: ?*gio.Icon = icon: {
    if (!self.window.config.gtk_tab_icons) break :icon null;
    if (position >= 10) break :icon null;
    
    // Logic here
    break :icon result;
};
```

Group related types and enums in a single containing struct for better organization:
```zig
// Instead of:
pub const ColorOperationSource = enum(u16) { /* ... */ };
pub const ColorOperationList = enum(u16) { /* ... */ };
pub const ColorOperationKind = enum(u16) { /* ... */ };

// Use a containing struct:
pub const ColorOperation = struct {
    pub const Source = enum(u16) { /* ... */ };
    pub const List = enum(u16) { /* ... */ };
    pub const Kind = enum(u16) { /* ... */ };
};
```

For public interfaces, consider separating functionality into distinct, purpose-specific functions rather than using boolean flags to modify behavior:
```zig
// Instead of:
pub fn init(self: *Window, app: *App, is_quick_terminal: bool) !void {
    // Complex conditional logic based on is_quick_terminal
}

// Prefer:
pub fn init(self: *Window, app: *App) !void {
    // Common initialization
}

pub fn initQuickTerminal(self: *Window, app: *App) !void {
    // Quick terminal specific initialization
}
```