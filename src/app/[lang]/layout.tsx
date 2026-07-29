import type { CSSProperties, ReactNode } from "react";
import { DocsLayout } from "fumadocs-ui/layouts/docs";
import { source } from "@/lib/source";
import { baseOptions, translations } from "@/lib/layout.shared";
import { DocsProviders } from "@/components/docs-providers";

// Owns the <html>/<body> shell so the lang attribute tracks the active locale.
export default async function Layout({
  params,
  children,
}: {
  params: Promise<{ lang: string }>;
  children: ReactNode;
}) {
  const { lang } = await params;

  const fallbackFonts = {
    "--font-serif": '"Instrument Serif", Georgia, serif',
    "--font-display": '"Space Grotesk", system-ui, sans-serif',
    "--font-sans": '"Archivo", system-ui, sans-serif',
    "--font-mono": '"Space Mono", ui-monospace, monospace',
  } as CSSProperties;

  return (
    <html lang={lang} suppressHydrationWarning>
      <body className="antialiased" style={fallbackFonts}>
        <DocsProviders i18n={translations.provider(lang)}>
          <DocsLayout {...baseOptions(lang)} tree={source.getPageTree(lang)}>
            {children}
          </DocsLayout>
        </DocsProviders>
      </body>
    </html>
  );
}
