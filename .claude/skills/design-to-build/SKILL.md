---
name: design-to-build
description: 從設計到實作一次做出一個頁面或元件：ui-designer 產出規格＋審查 rubric，astro-frontend-developer 依規格實作出第一版。Use when the user wants to design and build a page/component for this portfolio end-to-end（如「做一個 ProjectCard」「從設計到實作 About 頁」）。
---

# Design → Build（UI ＋ FE 協作）

把一個頁面或元件「從設計到實作」一次做出來：先讓 `ui-designer` 產出**規格 + 審查 rubric**，再讓 `astro-frontend-developer` 依規格實作出第一版。產物可直接交給 `/visual-review-loop` 打磨到達標。

## 何時用
使用者要新增或改一個頁面 / 元件。若只是要審查既有實作，改用 `/visual-review-loop`。

## 前置
1. 讀 `CLAUDE.md`（架構、技術選型）與 `DESIGN.md`（設計唯一來源）。
2. 確認目標：**哪個頁/元件、放什麼內容、對應哪個路由**。不清楚就先問使用者，別猜。

## 流程

### 1. 設計（agent：`ui-designer`）
用 Agent 啟動 `ui-designer`，要它把目標寫成 `docs/specs/<name>.md`，**內含兩部分**：
- **規格 Spec**：元件拆解、各容器/文字層的 token、light + dark 兩版、a11y、版面與間距節奏。一律用 `DESIGN.md` token 表達，不得寫死色票/間距。
- **審查 Rubric**：給 `/visual-review-loop` 評分用，務必含門檻、`[GATE]`、配分與量測方式（範本見下）。

若設計需要 `DESIGN.md` 沒有的新值，ui-designer 應**先提案修改 `DESIGN.md`**，不要塞進規格硬寫。

### 2. 實作（agent：`astro-frontend-developer`）
用 Agent 啟動 `astro-frontend-developer`，附上 `docs/specs/<name>.md`，要它：
- 依規格實作（`.astro` 為主；只有確有互動需求才用 React island，並選最省的 client directive）。
- token 走 `tailwind.config` 對應的語意化 class，不寫死值。
- `npm run build` 通過、無型別錯誤；有錯如實回報。

### 3. 交付
回報：做了什麼、檔案路徑、規格/rubric 路徑（`docs/specs/<name>.md`），並建議下一步跑 `/visual-review-loop <route>` 把它打磨到達標。

## 規格 + Rubric 範本（給 ui-designer 當輸出格式）

```md
# <元件/頁面名稱> Spec

## 規格
### 結構
- 容器：<token，如 card → bg surface / 1px border / rounded-lg / padding lg>
- <各文字層：typography token + 顏色 token + 間距>
- 狀態：hover / focus / active / disabled（以 token 描述）
### Dark 版
- <對應 dark token；accent 用 primary-bright>
### 版面
- <欄寬、間距節奏（4px scale）、響應式 1→2→3 欄等>
### a11y
- 對比 ≥ AA、focus 2px primary ring、tap target ≥ 44px、語意/heading 階層

## 審查 Rubric（/visual-review-loop 用）
- 門檻：總分 ≥ 90 / 100，且所有 [GATE] 必過。
- 最多迭代：3 輪。
- 量測以實際渲染為準（Chrome DevTools computed style / lighthouse / a11y tree / screenshot）。

| # | 類別 | 檢查項 | 量測方式 | 通過條件 | 配分 |
|---|------|--------|----------|----------|------|
| 1 | Token-色彩 | 各面/文字顏色 | getComputedStyle | 命中對應 token | 10 |
| 2 | Token-間距 | padding/margin/gap | getComputedStyle | = token px | 10 |
| 3 | Token-字體 | font-size/weight | getComputedStyle | 命中 typography token | 10 |
| 4 | Token-圓角 | border-radius | getComputedStyle | = rounded token | 5 |
| 5 | 版面/層次 | 對照規格 | screenshot 判讀 | 結構/間距節奏相符 | 15 |
| 6 | Dark parity | dark token + accent=primary-bright | computed style | 全部命中 | 15 |
| 7 | 響應式 | mobile/tablet/desktop | resize + screenshot | 無破版 | 10 |
| 8 [GATE] | 對比 | 文字對比 | lighthouse a11y | ≥ AA | 10 |
| 9 [GATE] | Console 乾淨 | 無 error | console messages | 0 error | 必過 |
| 10 [GATE] | Focus/鍵盤 | 可聚焦、ring 可見 | snapshot + screenshot | 達標 | 必過 |
| 11 | 效能/JS 量 | 非互動處 JS | network / lighthouse | 符合預期 | 5 |
```

> ui-designer 應依該元件實際情況增刪 rubric 列、調配分與 gate，但保留「門檻 + [GATE] + 量測方式」這個結構，確保 `visual-reviewer` 能照表評分。
