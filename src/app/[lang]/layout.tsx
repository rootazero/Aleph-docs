import type { ReactNode } from "react";
import { Instrument_Serif, Space_Grotesk, Archivo, Space_Mono } from "next/font/google";
import { DocsLayout } from "fumadocs-ui/layouts/docs";
import { source } from "@/lib/source";
import { baseOptions, translations } from "@/lib/layout.shared";
import { DocsProviders } from "@/components/docs-providers";

const serif = Instrument_Serif({
  variable: "--font-serif",
  subsets: ["latin"],
  weight: "400",
  style: ["normal", "italic"],
});
const display = Space_Grotesk({
  variable: "--font-display",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});
const sans = Archivo({
  variable: "--font-sans",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
});
const mono = Space_Mono({
  variable: "--font-mono",
  subsets: ["latin"],
  weight: ["400", "700"],
  style: ["normal", "italic"],
});

// Owns the <html>/<body> shell so the lang attribute tracks the active locale.
export default async function Layout({
  params,
  children,
}: {
  params: Promise<{ lang: string }>;
  children: ReactNode;
}) {
  const { lang } = await params;

  return (
    <html lang={lang} suppressHydrationWarning>
      <body className={`${serif.variable} ${display.variable} ${sans.variable} ${mono.variable} antialiased`}>
        <DocsProviders i18n={translations.provider(lang)}>
          <DocsLayout {...baseOptions(lang)} tree={source.getPageTree(lang)}>
            {children}
          </DocsLayout>
        </DocsProviders>
      </body>
    </html>
  );
}
