"use client";

import type { ReactNode } from "react";
import { RootProvider } from "fumadocs-ui/provider/base";
import { FrameworkProvider, type Framework } from "fumadocs-core/framework";
import {
  usePathname as useNextPathname,
  useRouter,
  useParams,
} from "next/navigation";
import Link from "next/link";
import Image from "next/image";

type RootProviderProps = React.ComponentProps<typeof RootProvider>;

// The default locale (en) is served prefix-free at the site root: the i18n
// middleware rewrites "/x" -> "/en/x" internally. Static generation therefore
// bakes usePathname() as "/en/x" into the prerendered HTML, while the browser
// path is "/x". Fumadocs resolves the active tree path (and the TOC "On this
// page" label) from usePathname(), so server and client disagreed for the
// hidden default locale — a hydration mismatch (React #418). zh keeps its
// explicit "/zh" prefix on both sides, so it was never affected.
//
// Normalising the baked default-locale prefix away makes both sides agree:
//   server "/en/x" -> "/x"   client "/x" -> "/x".
function useNormalizedPathname(): string {
  const pathname = useNextPathname();
  if (pathname === "/en") return "/";
  if (pathname.startsWith("/en/")) return pathname.slice("/en".length);
  return pathname;
}

// Mirrors fumadocs-ui/provider/next (NextProvider + base RootProvider) but with
// the locale-normalising usePathname above instead of next/navigation's raw one.
export function DocsProviders({
  i18n,
  children,
}: {
  i18n: RootProviderProps["i18n"];
  children: ReactNode;
}) {
  return (
    <FrameworkProvider
      usePathname={useNormalizedPathname}
      useRouter={useRouter}
      useParams={useParams}
      // Next's Link/Image typings differ from fumadocs' Framework members (href
      // is Url vs string); fumadocs' own NextProvider passes them through
      // untyped. Cast to match — runtime behaviour is identical.
      Link={Link as Framework["Link"]}
      Image={Image as Framework["Image"]}
    >
      {/* theme is disabled (light-only site); no .dark class on <html>. */}
      <RootProvider theme={{ enabled: false }} i18n={i18n}>
        {children}
      </RootProvider>
    </FrameworkProvider>
  );
}
