---
title: Align AI interfaces
description: 'When coding against LLM providers, treat model capabilities and prompt/tool
  formats as *spec-driven interfaces*: match upstream expectations exactly, and avoid
  ad-hoc mappings or manual edits that can drift.'
repository: earendil-works/pi
label: AI
language: TypeScript
comments_count: 3
repository_stars: 79783
---

When coding against LLM providers, treat model capabilities and prompt/tool formats as *spec-driven interfaces*: match upstream expectations exactly, and avoid ad-hoc mappings or manual edits that can drift.

Apply this as three concrete rules:
1) **Don’t hand-edit generated AI registries**
   - If a file is generated (e.g., `models.generated.ts`), update inputs/metadata at the source and regenerate via the build/generation script.

2) **Map “thinking/effort” (and similar) levels per model without collapsing semantics**
   - Prefer explicit per-model mappings based on what the provider/model truly supports.
   - Don’t blindly map a distinct level (e.g., `xhigh`) to a different one (e.g., `max`) unless the provider spec indicates they are equivalent.

   Example pattern:
   ```ts
   function mapThinkingLevelToEffort(modelId: string, level: string) {
     if (level !== "xhigh") return level;

     // Example: Opus 4.7 distinguishes xhigh vs max.
     const isOpus47 = ["opus-4-7", "opus-4.7"].some(s => modelId.includes(s));
     return isOpus47 ? "xhigh" : "max";
   }
   ```

3) **Match provider prompt/tool syntax exactly (use the same tag structure)**
   - When using provider-specific tools/structured sections, follow the provider’s documented markup.

   Example pattern:
   ```ts
   function buildSkillsSection(skills: string[]): string {
     if (skills.length === 0) return "";
     const body = skills.join("\n");
     return `<available_skills>\n${body}\n</available_skills>`;
   }
   ```

Net effect: fewer “it works for some models” surprises, less drift between code and provider reality, and safer changes when providers add/alter capabilities.