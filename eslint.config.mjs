// `eslint-config-next` 16 直接导出 flat config 数组，不再提供 eslintrc 风格的
// 可 extends 配置；用 `FlatCompat` 包一层会在配置加载阶段抛
// "Converting circular structure to JSON"（`eslint-plugin-react` 的插件对象是
// 循环引用，schema 校验失败后的报错格式化又把它 JSON.stringify 了一遍）。
// 所以这里直接吃它导出的 flat 数组。
import nextCoreWebVitals from "eslint-config-next/core-web-vitals";
import nextTypescript from "eslint-config-next/typescript";

const eslintConfig = [
  ...nextCoreWebVitals,
  ...nextTypescript,
  {
    ignores: [".next/**", ".source/**", "node_modules/**"],
  },
];

export default eslintConfig;
