import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Aleph Documentation",
  description: "Documentation for Aleph (ℵ) — a self-hosted polymorphic personal AI assistant built in Rust.",
};

// The <html>/<body> shell lives in app/[lang]/layout.tsx so <html lang> can
// follow the active locale (en/zh). This root layout only loads global styles;
// Next.js still requires a root layout to exist.
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return children;
}
