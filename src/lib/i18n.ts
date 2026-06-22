import { defineI18n } from "fumadocs-core/i18n";

// Standalone docs site i18n. English is the default and unprefixed
// ("/", "/gateway"); other languages are prefixed ("/zh", "/zh/gateway").
// hideLocale "default-locale" keeps English at the root. Locale routing is
// driven by the Fumadocs i18n middleware in src/proxy.ts.
export const i18n = defineI18n({
  defaultLanguage: "en",
  languages: ["en", "zh"],
  hideLocale: "default-locale",
  parser: "dir",
});
