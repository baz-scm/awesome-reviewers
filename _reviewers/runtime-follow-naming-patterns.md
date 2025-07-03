---
title: Follow naming patterns
description: 'Maintain consistent naming patterns throughout your code to improve
  readability and maintainability. Follow these guidelines:


  1. Use PascalCase for public methods and members'
repository: dotnet/runtime
label: Naming Conventions
language: C#
comments_count: 9
repository_stars: 16578
---

Maintain consistent naming patterns throughout your code to improve readability and maintainability. Follow these guidelines:

1. Use PascalCase for public methods and members
   ```csharp
   // Incorrect
   public static int iCreateProcessInfo() { ... }
   
   // Correct
   public static int CreateProcessInfo() { ... }
   ```

2. Method names should accurately reflect their purpose
   ```csharp
   // Misleading (doesn't return anything)
   public static void GetExtendedHelp(ParseResult _) { ... }
   
   // Better
   public static void DisplayHelp(ParseResult _) { ... }
   ```

3. Match related parameter names for clarity
   ```csharp
   // Inconsistent
   GetConnectionInfo(connection, out protocol, out cipherSuite, ref negotiatedAlpn, out alpnLength);
   
   // Consistent
   GetConnectionInfo(connection, out protocol, out cipherSuite, ref negotiatedAlpn, out negotiatedAlpnLength);
   ```

4. Design enums with meaningful defaults
   ```csharp
   // Poor design (default value is meaningful)
   public enum ExtendedLayoutKind
   {
       None = -1,
       CStruct = 0  // This becomes the default!
   }
   
   // Better design
   public enum ExtendedLayoutKind
   {
       None = 0,    // Default is semantically "none"
       CStruct = 1
   }
   ```

5. Use consistent abbreviations based on platform conventions
   ```csharp
   // Unnecessarily verbose when platform uses "Nw" consistently
   internal sealed class SafeNetworkFrameworkHandle : SafeHandleZeroOrMinusOneIsInvalid
   
   // Better
   internal sealed class SafeNwHandle : SafeHandleZeroOrMinusOneIsInvalid
   ```

When selecting names, consider how they'll be read in context and their alignment with existing patterns in your codebase and the platform.
