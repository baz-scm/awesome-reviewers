---
title: Distinguish Next.js routers
description: 'Always provide separate implementation instructions for Next.js App
  Router (13+) and Pages Router. These routing systems have different file structures,
  initialization requirements, and component placement:'
repository: mui/material-ui
label: Next
language: Markdown
comments_count: 4
repository_stars: 96063
---

Always provide separate implementation instructions for Next.js App Router (13+) and Pages Router. These routing systems have different file structures, initialization requirements, and component placement:

- **App Router**: Place components and configuration in the appropriate files within the `app` directory:
  ```tsx
  // app/layout.tsx for root configuration
  export default function RootLayout(props: { children: React.ReactNode }) {
    return (
      <html lang="en" suppressHydrationWarning>
        <body id="__next"> {/* Manually add ID for styling hooks */}
          <AppRouterCacheProvider options={{ enableCssLayer: true }}>
            {props.children}
          </AppRouterCacheProvider>
        </body>
      </html>
    );
  }
  ```

- **Pages Router**: Use custom files in the root directory:
  ```tsx
  // pages/_document.tsx (needs to be manually created)
  export default function Document() {
    return (
      <Html>
        <Head />
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
  ```

When documenting features, clearly indicate which router approach is being used and provide separate examples for each. Always note router-specific requirements like manually adding element IDs (`id="__next"`) for App Router that were automatically handled in earlier versions.