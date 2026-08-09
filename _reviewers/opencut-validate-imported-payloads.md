---
title: Validate imported payloads
description: When ingesting untrusted data (e.g., JSON pasted/uploaded by users),
  validate the *entire* payload against a schema (including nested structures) before
  writing to storage or otherwise trusting it. Avoid relying on top-level presence
  checks or unsafe type casts; these can let malformed nested content persist and
  only fail later.
repository: opencut-app/opencut
label: Security
language: TypeScript
comments_count: 1
repository_stars: 81817
---

When ingesting untrusted data (e.g., JSON pasted/uploaded by users), validate the *entire* payload against a schema (including nested structures) before writing to storage or otherwise trusting it. Avoid relying on top-level presence checks or unsafe type casts; these can let malformed nested content persist and only fail later.

Recommended practice:
- Define a schema for the expected shape (and deep sub-objects/arrays).
- Parse/validate the incoming value and handle failures by rejecting the import early.
- Persist the schema-validated/parsed result (not the original untyped object).
- Decide explicitly how to treat unknown/extra fields (e.g., tolerate for forward compatibility).

Example (Zod-style):
```ts
import { z } from "zod";

const importedProjectSchema = z.object({
  metadata: z.object({
    id: z.string(),
    name: z.string(),
    thumbnail: z.string().nullable().optional(),
    duration: z.number(),
    createdAt: z.string(),
    updatedAt: z.string(),
  }),
  scenes: z.array(
    z.object({
      id: z.string(),
      name: z.string(),
      isMain: z.boolean(),
      tracks: z.array(
        z.object({
          /* validate nested elements/structure here */
        })
      ),
      bookmarks: z.array(z.any()).optional(),
      createdAt: z.string(),
      updatedAt: z.string(),
    })
  ),
  settings: z.any(),
  timelineViewState: z.any(),
  currentSceneId: z.string(),
  version: z.number(),
});

async function importProjectFromJSON(jsonString: string) {
  const payload = JSON.parse(jsonString);
  const parsed = importedProjectSchema.safeParse(payload);
  if (!parsed.success) {
    toast.error("Invalid project file");
    return null;
  }

  // Persist only the validated parsed object
  await storageService.saveProject(parsed.data);
  return parsed.data.metadata.id;
}
```