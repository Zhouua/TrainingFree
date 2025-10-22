'use client';

import * as React from 'react';
import { ThemeProvider as NextThemesProvider } from 'next-themes';

export function ThemeProvider({
                                  children,
                                  attribute = "class",
                                  defaultTheme = "system",
                                  enableSystem = true,
                                  disableTransitionOnChange = false,
                                  ...props
                              }: {
    children: React.ReactNode;
    attribute?: "class";
    defaultTheme?: "light" | "dark" | "system";
    enableSystem?: boolean;
    disableTransitionOnChange?: boolean;
}) {
    return (
        <NextThemesProvider
            attribute={attribute}
            defaultTheme={defaultTheme}
            enableSystem={enableSystem}
            disableTransitionOnChange={disableTransitionOnChange}
            {...props}
        >
            {children}
        </NextThemesProvider>
    );
}