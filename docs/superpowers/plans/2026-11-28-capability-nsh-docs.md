# Capability and NSH Panel Documentation Implementation Plan

Status: complete. The bilingual documentation gates and production route checks passed.

**Goal:** Align the public bilingual documentation with the Capability architecture and the NSH desktop release.

**Architecture:** Use a Capability overview for the design principle and delegate contract details to the existing reference pages. Describe the NSH host, shared browser renderer, and optional TSX AppView from their actual launch and packaging paths.

**Tech Stack:** Fumadocs MDX, Next.js, Python documentation gates, Aleph Rust and TypeScript source.

**Spec:** [Capability and NSH documentation design](../specs/2026-11-28-capability-nsh-docs-design.md)

## Global Constraints

- Source revision `1b959fdf46f592928aa3143b8dcf99798551391d`.
- English and Chinese share routes, navigation coverage, and heading structure.
- NSH 0.6.0 ships the shared Leptos/WASM Panel. TSX AppView requires macOS and `tsx-panel`.
- Keep legitimate plugin WASM references and dated change history. Retire current Tauri guidance and old duplicate concepts.
- Keep the gate baseline at zero. Validate the site against `../Aleph`.

## Review Focus

- Follow old `/concepts/capability-system` and `/concepts/extension-system` URLs in both locales and verify redirects to real pages.
- Trace the same renderer from Gateway `/` through desktop startup and production packaging. Verify that the source build still generates shared Web assets.
- Verify the Capability kind and facet distinction, including descriptor-only kinds and runtime permissions.
- Verify that Shell docs describe the paired Bash JSONL route and the reach of other shell modes using shipped schemas and effect guards.
- Check that changelog dates and versions distinguish merged changes from releases and that WebChat, Panel and WASM plugins retain their own build or runtime paths.

## Task 1 — Capability overview and concept consolidation

**Files:** Under `content/docs/en/` and `content/docs/zh/`, create `capabilities/overview.mdx`, update `capabilities/capability-model.mdx`, `capabilities/meta.json`, and `concepts/extensions.mdx`, delete `concepts/capability-system.mdx` and `concepts/extension-system.mdx`, and update `concepts/meta.json` and references. Add four redirects in `next.config.ts`.

- [x] Record the duplicate routes and the current Capability descriptor/backend support from source.
- [x] Introduce the principle and the discovery, call, replacement, subscription and management paths. Move current declaration, runtime, plugin adapter, priority and lifecycle details to their canonical pages.
- [x] Retire duplicate pages and fix links. Redirect the old capability page to `/capabilities/overview` and the old extension system page to `/concepts/extensions`, with `/zh` equivalents.
- [x] Run the structure and bilingual gates. Expect zero findings. Verify redirects with a production server in Task 3.

## Task 2 — NSH desktop and shared Panel

**Files:** Under both locale roots update `desktop-hosts/{overview,panel,panel-runtime,plugin-ui}.mdx`, `interfaces/webchat.mdx`, `development/building.mdx`, `architecture/{overview,1-2-3-4-model,gateway}.mdx`, `api/rust.mdx`, `getting-started/{installation,quick-start}.mdx`, `terminology.mdx`, and `index.mdx`. Adjust other live references found by the inventory.

- [x] Check `desktop/nsh-shell/src/{app,cli,local_service,panel_bridge}.rs`, the release workflow, `justfile`, and the Gateway resource and transport code.
- [x] Replace old shell claims and eliminate current Tauri headings. Explain bundled and remote server modes, NSH bridge and packaging, shared WebChat assets and the opt-in TSX route with code anchors.
- [x] Run the anchor and symbol gates. Expect no desktop or Panel regressions. Run the upstream Panel dist and WebView baseline scripts.

## Task 3 — Close drift and verify the site

**Files:** Under both locale roots update `tools/builtin.mdx`, `architecture/sandbox.mdx`, `concepts/memory.mdx`, the Gateway method pages for chat and graph, and `changelog.mdx`.

- [x] Replace stale shell implementation status using the merged schema and source constraints. Document `chat.models.list` and `graph.mutate_note` under their method families. Reconcile the memory helper with the current implementation.
- [x] Add the desktop, Capability, and Panel changes to bilingual unreleased history with matching dates.
- [x] Run `python3 scripts/run_gates.py --repo ../Aleph --build` and `git diff --check`. Every gate passed with clean whitespace.
- [x] Verify four 308 redirects and eight 200 documentation responses on the production build. Check rendered titles, shared renderer details, homepage links, and the updated concept links in both locales.
