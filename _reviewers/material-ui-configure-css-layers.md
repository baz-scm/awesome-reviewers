---
title: Configure CSS layers
description: When integrating Material UI with other styling solutions like Tailwind
  CSS v4, proper configuration of CSS layers is essential to ensure correct style
  precedence and override behavior.
repository: mui/material-ui
label: Configurations
language: Markdown
comments_count: 5
repository_stars: 96063
---

When integrating Material UI with other styling solutions like Tailwind CSS v4, proper configuration of CSS layers is essential to ensure correct style precedence and override behavior.

Follow these framework-specific steps to enable and configure CSS layers:

1. **Client-side applications (Vite/SPA)**:
   ```tsx
   import { StyledEngineProvider } from '@mui/material/styles';
   import GlobalStyles from '@mui/material/GlobalStyles';

   ReactDOM.createRoot(document.getElementById('root')!).render(
     <React.StrictMode>
       <StyledEngineProvider enableCssLayer>
         <GlobalStyles styles="@layer theme, base, mui, components, utilities;" />
         {/* Your app */}
       </StyledEngineProvider>
     </React.StrictMode>,
   );
   ```

2. **Next.js App Router**:
   ```tsx
   import { AppRouterCacheProvider } from '@mui/material-nextjs/v15-appRouter';
   import GlobalStyles from '@mui/material/GlobalStyles';

   export default function RootLayout() {
     return (
       <html lang="en" suppressHydrationWarning>
         <body>
           <AppRouterCacheProvider options={{ enableCssLayer: true }}>
             <GlobalStyles styles="@layer theme, base, mui, components, utilities;" />
             {/* Your app */}
           </AppRouterCacheProvider>
         </body>
       </html>
     );
   }
   ```

3. **Next.js Pages Router**:
   ```tsx
   import { AppCacheProvider } from '@mui/material-nextjs/v15-pagesRouter';
   import GlobalStyles from '@mui/material/GlobalStyles';

   export default function MyApp(props: AppProps) {
     const { Component, pageProps } = props;
     return (
       <AppCacheProvider {...props}>
         <GlobalStyles styles="@layer theme, base, mui, components, utilities;" />
         <Component {...pageProps} />
       </AppCacheProvider>
     );
   }
   ```

Always ensure that the `mui` layer comes before the `utilities` layer so that utility classes can properly override Material UI styles without using the `!important` directive.