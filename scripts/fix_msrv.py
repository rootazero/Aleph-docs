#!/usr/bin/env python3
"""把文档站里过时的 Rust MSRV 数字（1.95 / 1.96.0）更新为当前真实值 1.99 / 1.99.1。

真值来源：Aleph 仓根 `Cargo.toml` 的 `rust-version = "1.99"` 与
`rust-toolchain.toml` 的 `channel = "1.99.1"`。

只处理本脚本列出的文件与字面量；命中数为 0 就报错退出。
"""

from __future__ import annotations

import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "content" / "docs"

# (相对路径, [(旧字面量, 新字面量), ...])
EDITS: list[tuple[str, list[tuple[str, str]]]] = [
    (
        "zh/development/design-patterns.mdx",
        [
            ("### Rust toolchain 1.95+", "### Rust toolchain 1.99+"),
            (
                "26.7.x：`rust-version` 在 Cargo.toml 已抬到 **1.95**。开发时使用 `rustup install 1.95` 或 `rust-toolchain.toml`。",
                "当前 `rust-version` 是 **1.99**，`rust-toolchain.toml` 把工具链固定到 `1.99.1`（含 `rustfmt`、`clippy` 与 `wasm32-unknown-unknown` 目标）。开发时用 `rustup install 1.99`，或直接依赖 `rust-toolchain.toml`。",
            ),
        ],
    ),
    (
        "zh/development/testing.mdx",
        [
            ("### Rust toolchain 1.95+", "### Rust toolchain 1.99+"),
            (
                "26.7.x：`rust-version` 在 Cargo.toml 已抬到 **1.95**。开发时使用 `rustup install 1.95` 或 `rust-toolchain.toml`。",
                "当前 `rust-version` 是 **1.99**，`rust-toolchain.toml` 把工具链固定到 `1.99.1`（含 `rustfmt`、`clippy` 与 `wasm32-unknown-unknown` 目标）。开发时用 `rustup install 1.99`，或直接依赖 `rust-toolchain.toml`。",
            ),
        ],
    ),
    (
        "zh/getting-started/quick-start.mdx",
        [("从源码构建需要 Rust 1.95+。", "从源码构建需要 Rust 1.99+。")],
    ),
    (
        "zh/getting-started/installation.mdx",
        [("- Rust 1.95+（以根 `Cargo.toml` 的 `rust-version` 为准）", "- Rust 1.99+（以根 `Cargo.toml` 的 `rust-version` 为准）")],
    ),
    (
        "zh/getting-started/deployment.mdx",
        [("1. 使用 Rust 1.95+ 构建 `aleph-server`；", "1. 使用 Rust 1.99+ 构建 `aleph-server`；")],
    ),
    (
        "zh/index.mdx",
        [
            ("# 从源码构建核心（Rust 1.95+）", "# 从源码构建核心（Rust 1.99+）"),
            (
                'description="从源代码构建（Rust 1.95+）、测试、贡献与设计模式"',
                'description="从源代码构建（Rust 1.99+）、测试、贡献与设计模式"',
            ),
        ],
    ),
    (
        "en/development/design-patterns.mdx",
        [
            ("### Rust Toolchain 1.95+", "### Rust Toolchain 1.99+"),
            (
                "26.7.x: `rust-version` in `Cargo.toml` has been bumped to **1.95**. Use `rustup install 1.95` or `rust-toolchain.toml` in development.",
                "The current `rust-version` is **1.99**, and `rust-toolchain.toml` pins the toolchain to `1.99.1` (with `rustfmt`, `clippy`, and the `wasm32-unknown-unknown` target). Use `rustup install 1.99`, or rely on `rust-toolchain.toml`.",
            ),
        ],
    ),
    (
        "en/development/testing.mdx",
        [
            ("### Rust Toolchain 1.95+", "### Rust Toolchain 1.99+"),
            (
                "26.7.x: `rust-version` in `Cargo.toml` has been bumped to **1.95**. Use `rustup install 1.95` or `rust-toolchain.toml` in development.",
                "The current `rust-version` is **1.99**, and `rust-toolchain.toml` pins the toolchain to `1.99.1` (with `rustfmt`, `clippy`, and the `wasm32-unknown-unknown` target). Use `rustup install 1.99`, or rely on `rust-toolchain.toml`.",
            ),
        ],
    ),
    (
        "en/getting-started/quick-start.mdx",
        [("Building from source requires Rust 1.95+.", "Building from source requires Rust 1.99+.")],
    ),
    (
        "en/getting-started/installation.mdx",
        [("- Rust 1.95+ as declared by `rust-version` in the root `Cargo.toml`", "- Rust 1.99+ as declared by `rust-version` in the root `Cargo.toml`")],
    ),
    (
        "en/getting-started/deployment.mdx",
        [("1. build `aleph-server` with Rust 1.95+;", "1. build `aleph-server` with Rust 1.99+;")],
    ),
    (
        "en/index.mdx",
        [
            ("# Build the core from source (Rust 1.95+)", "# Build the core from source (Rust 1.99+)"),
            (
                'description="Building from source (Rust 1.95+), testing, contributing, and design patterns"',
                'description="Building from source (Rust 1.99+), testing, contributing, and design patterns"',
            ),
        ],
    ),
]


def main() -> int:
    failures: list[str] = []
    for rel, pairs in EDITS:
        path = DOCS / rel
        text = path.read_text(encoding="utf-8")
        for old, new in pairs:
            count = text.count(old)
            if count != 1:
                failures.append(f"{rel}: 期望命中 1 次，实际 {count} 次：{old!r}")
                continue
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")
        print(f"ok {rel}")

    if failures:
        print("\n未完成：")
        for line in failures:
            print(f"  - {line}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
