---
title: Avoid localStorage for credentials
description: Do not store user profiles, authentication tokens, or other sensitive
  user information in client-side storage mechanisms like localStorage or sessionStorage.
  This creates security vulnerabilities as these storage mechanisms are accessible
  to any JavaScript running on the page, including potential XSS attacks.
repository: prowler-cloud/prowler
label: Security
language: TypeScript
comments_count: 1
repository_stars: 11834
---

Do not store user profiles, authentication tokens, or other sensitive user information in client-side storage mechanisms like localStorage or sessionStorage. This creates security vulnerabilities as these storage mechanisms are accessible to any JavaScript running on the page, including potential XSS attacks.

Instead:
1. Use server-side session management
2. Utilize memory-only state for the current session
3. Pass user data via React Context when needed across components
4. Consider established authentication libraries that implement security best practices

Example - Instead of:
```typescript
export const useUser = create(
  persist<UserStore>(
    (set) => ({
      user: null,
      setUser: (user) => set({ user }),
      clearUser: () => set({ user: null }),
    }),
    { name: 'user-storage', storage: createJSONStorage(() => localStorage) }
  )
);
```

Use a context-based approach:
```typescript
// In a shared layout or provider
export const UserContext = createContext<UserProfileProps | null>(null);

export function UserProvider({ children }) {
  const { data } = useSession();  // Using an existing session management solution
  return <UserContext.Provider value={data?.user ?? null}>{children}</UserContext.Provider>;
}

// In components
export function useUser() {
  return useContext(UserContext);
}
```