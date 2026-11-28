import type { NextConfig } from "next";
import { createMDX } from "fumadocs-mdx/next";

const withMDX = createMDX();

const nextConfig: NextConfig = {
  async redirects() {
    return ["", "/zh"].flatMap((locale) => [
      {
        source: `${locale}/concepts/capability-system`,
        destination: `${locale}/capabilities/overview`,
        permanent: true,
      },
      {
        source: `${locale}/concepts/extension-system`,
        destination: `${locale}/concepts/extensions`,
        permanent: true,
      },
    ]);
  },
};

export default withMDX(nextConfig);
