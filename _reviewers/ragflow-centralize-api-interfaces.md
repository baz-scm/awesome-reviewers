---
title: Centralize API Interfaces
description: 'Enforce consistent API client construction: (1) centralize all REST
  endpoint paths and interface definitions in a shared module (e.g., `api.ts`) to
  prevent scattered string literals, and (2) when reading/writing request inputs like
  query params, use the correct standard APIs and keep TypeScript types aligned.'
repository: infiniflow/ragflow
label: API
language: TypeScript
comments_count: 2
repository_stars: 80174
---

Enforce consistent API client construction: (1) centralize all REST endpoint paths and interface definitions in a shared module (e.g., `api.ts`) to prevent scattered string literals, and (2) when reading/writing request inputs like query params, use the correct standard APIs and keep TypeScript types aligned.

Apply as follows:
- In services, import route builders/constants instead of embedding `'/api/v1/...` strings.
- For query params, don’t treat `URLSearchParams` as a plain object; iterate via `searchParams.entries()` and type-check values.

Example:
```ts
// web/src/api.ts
export const API_PREFIX = '/api/v1';
export const skillSpaceRoutes = {
  list: () => `${API_PREFIX}/skills/spaces`,
  detail: (spaceId: string) => `${API_PREFIX}/skills/spaces/${spaceId}`,
};

// web/src/services/skill-space-service.ts
import request from '@/utils/request';
import { skillSpaceRoutes } from '@/api';

class SkillSpaceService {
  private async request<T>(method: string, url: string, data?: any, params?: any): Promise<T> {
    const response: any = await request(url, { method: method as any, data, params });
    const jsonData = response?.data ?? response;
    if (jsonData?.code !== 0) throw new Error(jsonData?.message || 'Request failed');
    return jsonData.data;
  }

  async listSpaces() {
    return this.request<{ spaces: any[]; total: number }>('GET', skillSpaceRoutes.list());
  }
}
```

And for query params:
```ts
const getParams = (searchParams: URLSearchParams) => {
  const out: Record<string, string> = {};
  for (const [key, value] of searchParams.entries()) {
    out[key] = value;
  }
  return out;
};
```