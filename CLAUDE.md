# CLAUDE.md

個人 portfolio 網站。本檔記錄專案的技術選型與部署決策，供後續開發遵循。

## 專案性質

- 個人 portfolio / homepage，**多頁**（首頁 + About + Projects 等靜態頁），**目前無 blog**。
- 內容為主、互動極少（預期僅 dark/light 切換、手機選單之類）。
- 設計系統的單一來源是 `DESIGN.md`（colors / typography / spacing / rounded / components token）。

## 技術選型（已定案）

| 層 | 選擇 | 備註 |
|---|---|---|
| 框架 | **Astro** | 內容型網站，預設輸出純 HTML、起始 JS ~0KB；多頁為原生支援。 |
| UI 互動 | **React（Astro islands）** | 需要互動的元件用 React 寫，僅該元件 hydrate；其餘維持靜態。 |
| 樣式 | **Tailwind CSS v4** | `DESIGN.md` 的 token 對應進 `src/styles/global.css` 的 `@theme`（v4 無 `tailwind.config`），設計與程式同一來源。 |
| 語言 | **TypeScript** | |
| 內容 | Markdown / MDX（Astro Content Collections） | 目前無 blog；若日後要文章列表再啟用。 |

**選 Astro 而非純 React SPA 的理由**：本站多頁、幾乎不互動，純 SPA 會強迫訪客先下載整包 React 才看到內容，對 portfolio 的首次載入不划算。Astro 預設零 JS，需互動處再以 React island 局部加上，能完整沿用既有 React 能力。

> **版本注意**：Astro 釘在 **v5**（`astro@^5` + `@astrojs/react@^4`）。Astro 6 預設改用 rolldown-vite，與 `@tailwindcss/vite` 目前不相容（build 會報 `Missing field tsconfigPaths`）。升到 Astro 6 前須先確認此問題已解。

## 部署（已定案）

- **程式碼**：放 GitHub。
- **部署平台**：**Cloudflare Pages**（連結 GitHub repo，`git push` 後自動 build & deploy）。
- 選 Cloudflare Pages 而非 GitHub Pages 的理由：網域已在 Cloudflare，整合同源、免處理 SSL；且每個 PR/branch 自動產生 preview 網址。
- 開發流程不變：照常用 GitHub 存碼、開 PR、push；build 與上線由 Cloudflare 負責。

### 注意事項
- 若改回走 GitHub Pages：Cloudflare SSL/TLS 必須設 **Full**（用 Flexible 會無限重導向），並在 `public/CNAME` 放自訂網域。
- Cloudflare Pages 讀 private repo 需授權。

## 網站架構

### 頁面 / 路由
- `/`（index）— Hero（`headline-display` 姓名/標語）+ 精選 projects + 簡短 about + 聯絡。
- `/projects` — 全部專案列表，1→2→3 欄 grid，用 ProjectCard。
- `/about` — 經歷、技能、連結，單欄 prose（~720px）。
- 導覽：Home / Projects / About + 聯絡連結 + light/dark 切換。
- 日後可加 `/projects/[slug]` 專案詳情；目前無 blog。

### 目錄結構（Astro）
```
src/
  pages/            路由檔（index.astro、about.astro、projects/index.astro）
  layouts/          BaseLayout.astro（<head>、字型、nav、footer、主題初始化腳本）
  components/        靜態 .astro 元件（Hero、ProjectCard、Section…）
    islands/        React 互動元件（ThemeToggle、MobileMenu）— 唯一會 hydrate 的東西
  content/          Content Collections：projects/（.md/.mdx）+ config.ts schema
  styles/           global.css（Tailwind v4 入口 + @theme：DESIGN.md token 對應、@font-face）
  lib/              共用 TS utils（需要才建）
  content.config.ts Content Collections schema（projects）
public/             靜態資產、自架字型(woff2)、favicon
docs/specs/         ui-designer 產出的規格 + rubric（<name>.md）
astro.config.mjs    integrations：react、sitemap；vite plugin：@tailwindcss/vite
```

### 內容模型
- 專案資料用 Content Collection `projects`，frontmatter schema：`title`、`description`、`tech: string[]`、`links: { label, href }[]`、`cover?`、`featured?: boolean`、`order?: number`。
- 首頁精選取 `featured` 為真者；`/projects` 取全部，依 `order` 排序。

### 設計 token 對應
- `src/styles/global.css` 的 `@theme` 從 `DESIGN.md` 對應 `--color-*` / `--spacing-*` / `--radius-*` / `--text-*`（每個字級含 line-height·letter-spacing·font-weight）/ `--font-*`。Tailwind v4 沒有 `tailwind.config`。
- 元件只用語意化 class（`bg-surface`、`text-on-surface-muted`、`p-lg`、`rounded-lg`、`text-headline-sm`），不寫死色票/間距。
- 元件清單鏡射 `DESIGN.md` 的 components：button-primary/secondary、card、input、tag、code-block、link、nav。

## 開發協作流程（agents / skills）

本專案用三個 subagent 分工，並以兩個 skill 串起流程：

- **agents**
  - `ui-designer` — 視覺與設計系統守門人，產出規格與審查 rubric（以 `DESIGN.md` 為唯一來源）。
  - `astro-frontend-developer` — 依規格實作（Astro / React islands / Tailwind）。
  - `visual-reviewer` — 用 Chrome DevTools 量測渲染、對 rubric 評分，對 source code 唯讀。
- **`/design-to-build`** — 設計 → 實作。ui-designer 產出 `docs/specs/<name>.md`（規格＋rubric），frontend 依規格做出第一版。
- **`/visual-review-loop`** — 渲染審查 loop。起 dev server，visual-reviewer 對 rubric 用 Chrome DevTools 評分，未達門檻就把缺失丟回 frontend 修，迭代到分數過門檻（預設 ≥ 90/100 且所有 [GATE] 通過，最多 3 輪）。

**rubric 是兩個 skill 的交接物**：`design-to-build` 階段由 UI 寫出，`visual-review-loop` 階段拿來評分。

## 開發慣例

- 樣式一律走 Tailwind + `DESIGN.md` token，不要在元件裡寫死色票/間距魔術數字。
- 預設靜態；只有真的需要互動才引入 React island，避免無謂的 client JS。
