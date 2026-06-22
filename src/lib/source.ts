import { docs } from "@/.source/server";
import { loader } from "fumadocs-core/source";
import { i18n } from "./i18n";

// Docs are served at the site root (baseUrl "/"), so URLs are clean:
// "/" + "/gateway" (en), "/zh" + "/zh/gateway" (zh).
export const source = loader({
  baseUrl: "/",
  source: docs.toFumadocsSource(),
  i18n,
});
