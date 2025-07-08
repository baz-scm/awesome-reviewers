---
title: Maintain component consistency
description: 'Use a consistent approach when working with components to improve code
  maintainability and ensure visual coherence throughout the application:


  1. **Reuse existing components** rather than creating new ones for similar functionality.'
repository: prowler-cloud/prowler
label: Code Style
language: TSX
comments_count: 4
repository_stars: 11834
---

Use a consistent approach when working with components to improve code maintainability and ensure visual coherence throughout the application:

1. **Reuse existing components** rather than creating new ones for similar functionality.
   ```tsx
   // Good: Using the existing ContentLayout component
   <ContentLayout title="Configure Chatbot" icon="lucide:settings">
     {/* Content here */}
   </ContentLayout>
   
   // Avoid: Creating new custom layouts for similar purposes
   ```

2. **Centralize styling through component props** (color, variant, size) rather than adding custom classes:
   ```tsx
   // Good: Using standard props for styling
   <CustomLink
     path="/manage-groups"
     ariaLabel="Manage Groups"
     variant="dashed"
     color="secondary"
   />
   
   // Avoid: Adding custom classes that override the component's design system
   <CustomLink
     path="/manage-groups"
     className="rounded-md px-4 py-2 !font-bold hover:border-solid hover:bg-default-100"
   />
   ```

3. **Extract reusable code** into helper files when functionality is needed across multiple components:
   ```tsx
   // Good: Create shared helpers for reusable functionality
   // In a helper file:
   export const PermissionIcon = ({ enabled }: { enabled: boolean }) => (
     // Icon implementation
   );
   
   // Then import in multiple components:
   import { PermissionIcon } from "@/helpers/permission-helpers";
   ```

4. **Maintain separation between different component types** rather than merging them into one:
   ```tsx
   // Good: Separate components for different HTML elements
   <CustomInput type="text" {...props} />
   <CustomTextArea {...props} />
   
   // Avoid: Conditionally rendering different elements within one component
   <CustomInput type={type === "textarea" ? "textarea" : "text"} {...props} />
   ```

Following these principles ensures consistent UI patterns, reduces technical debt, and makes the codebase easier to maintain as it grows.