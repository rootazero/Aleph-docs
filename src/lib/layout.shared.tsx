import type { BaseLayoutProps } from "fumadocs-ui/layouts/shared";
import { defineI18nUI } from "fumadocs-ui/i18n";
import { i18n } from "./i18n";

// Fumadocs UI translations API. English is the framework default; only the
// Chinese overrides are provided. `displayName` labels the language toggle.
// Consumed via i18nProvider(translations, locale) in the [lang] layout.
export const translations = defineI18nUI(i18n, {
  en: { displayName: "English" },
  zh: {
    displayName: "中文",
    search: "搜索文档",
    searchNoResult: "没有找到结果",
    toc: "目录",
    lastUpdate: "最后更新",
    previousPage: "上一页",
    nextPage: "下一页",
    chooseLanguage: "选择语言",
  },
});

// Locale-aware path prefix: en -> "" (root), zh -> "/zh".
function prefix(lang: string): string {
  return lang === "en" ? "" : `/${lang}`;
}

// The marketing homepage is a separate deployment.
const SITE = "https://www.heyaleph.com";

export function baseOptions(lang: string): BaseLayoutProps {
  const docsHome = prefix(lang) || "/";

  return {
    nav: {
      title: (
        <>
          <span
            aria-hidden="true"
            style={{
              display: "inline-block",
              width: "1.3em",
              height: "1.3em",
              borderRadius: "50%",
              backgroundImage: "url('/aleph-glyph.svg')",
              backgroundSize: "cover",
              backgroundRepeat: "no-repeat",
              backgroundPosition: "center",
              verticalAlign: "-0.32em",
              marginInlineEnd: "0.5rem",
            }}
          />
          Aleph
        </>
      ),
      url: docsHome,
    },
    // Light-only site: hide the theme toggle.
    themeSwitch: {
      enabled: false,
    },
    links: [
      {
        text: lang === "zh" ? "首页" : "Home",
        url: `${SITE}${prefix(lang)}`,
        external: true,
      },
      {
        text: "GitHub",
        url: "https://github.com/rootazero/Aleph",
        external: true,
      },
    ],
  };
}
