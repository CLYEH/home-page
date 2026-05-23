# ProjectCard — 規格 + 審查 Rubric

> 設計唯一來源：`/Users/clyeh/home-page/DESIGN.md`。token 程式對應：`src/styles/global.css` 的 `@theme`（Tailwind v4，無 `tailwind.config`）。
> 本檔只用既有 token 名 / 語意化 class，**不寫死色票或魔術數字**。任何 DESIGN.md 未涵蓋的值都以「提案新增 token」處理（見最後一節），不硬寫進規格。

---

## 用途

- 主場景：`/projects` 頁的 1→2→3 欄 grid 卡片。
- 重用：首頁「精選」區（取 `featured` 的同一元件，外觀不變）。
- 一個元件、一份外觀；兩個頁面只是放在不同 grid 容器裡。

## 資料欄位（對應 projects content collection schema）

| 欄位 | 型別 | 必填 | 呈現 |
|---|---|---|---|
| `title` | string | 必填 | 卡片標題（主連結） |
| `description` | string | 必填 | 描述段落 |
| `tech` | string[] | 選填（可空陣列） | tag 樣式 chip 列 |
| `links` | `{ label, href }[]` | 選填（可空陣列） | link 樣式（如 "View" / "Source"） |
| `cover` | image / string | 選填 | 有值才顯示，置於卡片最上方 |

---

# Part 1 — 規格 Spec

## 1.1 結構（由外到內，標註 token）

```
article.card                ← 容器：card token
├─ figure (cover, 選填)      ← 封面圖區，僅 cover 有值時渲染
│   └─ img                   ← rounded-md、object-cover、1px border
├─ h3  (title)               ← headline-sm，內含主連結 <a>（見 1.6 整卡可點）
├─ p   (description)         ← body-md / on-surface-muted
├─ ul  (tech tags, 選填)     ← tag chip 列；tech 為空則整塊不渲染
└─ nav/div (links, 選填)     ← link 樣式列；links 為空則整塊不渲染
```

各層 token：

| 層 | token / class | 說明 |
|---|---|---|
| 容器 `article.card` | `bg-surface` · `border` 1px `border-border` · `rounded-lg`(12px) · `p-lg`(24px) | DESIGN.md `card` token 原樣。**不加陰影。** |
| 容器內縱向節奏 | `gap-md`(16px)（建議用 `flex flex-col gap-md`） | 元件內間距用 `md`，符合「元件內 16px」節奏 |
| cover `figure` | `rounded-md`(8px) · `overflow-hidden` · `border` 1px `border-border` | 圖片 `lg` 圓角是給獨立大圖；卡片內封面收斂為 `md`，且圖與卡 `p-lg` 內緣對齊。封面與標題間距由容器 `gap-md` 提供 |
| cover `img` | `w-full` · `aspect-[16/9]` · `object-cover` | 固定比例避免 grid 跳動；`16/9` 為建議比例（提案 token，見末節） |
| 標題 `h3` | `text-headline-sm`(20px/600) · `text-on-surface` | DESIGN.md「card titles」用 `headline-sm` |
| 標題連結 `a` | 文字色繼承 `on-surface`（非 link 藍）· focus ring（見 1.4） | 標題是主連結但**不染成 link 藍**：藍色 accent 須克制；卡片整體已是互動面，標題保持中性閱讀色，hover 時靠 border 變色傳達可點 |
| 描述 `p` | `text-body-md`(16px) · `text-on-surface-muted` · `line-clamp-3` | 標題↔描述間距 `gap-md`；建議 `line-clamp-3` 控高度，保 grid 列對齊 |
| tech tag `ul` | `flex flex-wrap gap-sm`(8px) | tag 之間 `sm`(8px)；與上方描述間距 `gap-md` |
| tech tag chip `li` | `tag` token：`bg-primary-subtle` · `text-primary` · `rounded-full` · `text-label-sm`(12px/500，tracking 0.04em) · 內距對齊 `tag`（左右 12px / 高 28px） | DESIGN.md `tag` token 原樣。tag 高 28px 純展示、非 tap target |
| links 區 `div` | `flex flex-wrap gap-md`(16px) | link 之間留 `md`(16px) 給足 tap 間距；與上方 tag 列間距 `gap-md` |
| link `a` | `link` token：`text-primary` · 平時 `no-underline` · hover `underline` · `text-label-md`(14px/500) | DESIGN.md `link` token；`label-md` 對齊「buttons and navigation links」字級 |

### 區塊出現/隱藏規則
- `cover` 無值 → 不渲染 `figure`，標題即為卡片第一個元素。
- `tech` 空 → 不渲染 tag `ul`。
- `links` 空 → 不渲染 links 區。
- 任一區塊隱藏時，靠容器 `gap-md` 自然收合，**不留空白佔位**。

## 1.2 版面（grid 行為與內部節奏）

- **外部 grid（容器負責，非本元件）**：`/projects` 與首頁精選都用 1→2→3 欄、欄間 `gap-lg`(24px)，呼應 DESIGN.md「project grid、24px(`lg`) gutter、~1120px 置中」。本元件只需 `w-full`、`h-full`，把對齊交給 grid。
- **等高對齊**：卡片用 `flex flex-col h-full`，描述 `line-clamp-3`；links 區可用 `mt-auto` 推到底，使同列卡片的 link 列底邊對齊（cover/描述長度不一時仍整齊）。
- **內部節奏**：容器內統一 `gap-md`(16px)；tag 內部 `gap-sm`(8px)。**只用 `sm` / `md` 兩級**，維持元件內 4px-scale 的克制節奏，不引入中間值。
- **斷點**：
  - mobile（1 欄）：卡片滿欄、`p-lg` 維持、body 16px、cover `aspect-[16/9]`。
  - 2 欄（≈ md）/ 3 欄（≈ lg）：卡片寬度由 grid 決定，內距與節奏不變（不因變窄而縮 padding）。
- **密度**：低。寧可加留白也不塞。卡片不設 `max-height`；高度由內容 + `line-clamp` 決定。

## 1.3 狀態 — hover

- **整卡 hover**：border `border` → `primary`（dark：`border-dark` → `primary-bright`）。
  - 實作：`hover:border-primary`（dark：`dark:hover:border-primary-bright`）。
  - **不加陰影、不位移、不縮放、不變背景**——層次只靠 border 顏色位移（DESIGN.md「raise emphasis by shifting the border toward primary rather than adding shadow」）。
- **link hover**：個別 link 出現 `underline`（`text-primary` 不變）。
- **動效**：`transition-colors`（≈150ms）只過渡顏色；尊重 `prefers-reduced-motion`（reduce 時可關閉過渡）。

## 1.4 狀態 — focus / 鍵盤

- **focus 可見**：用 `:focus-visible`，2px ring，`primary`（dark：`primary-bright`），**非 glow**。建議 `focus-visible:outline-2 focus-visible:outline-primary focus-visible:outline-offset-2`（dark 換 `primary-bright`）。
- **Tab 順序（單張卡內）**：
  1. 標題主連結（卡片的主目的地）
  2. 各 `links`（View / Source…）依序
  - tag chip **非互動**、不可聚焦（無 `href`、無 `tabindex`）。
- 標題主連結 focus 時，ring 應環繞**標題文字**（即可見聚焦區）即可；不要求整卡描邊（避免與 hover 的整卡 border 變色語意打架）。
- 所有可聚焦元素皆有可見 focus 樣式，無 `outline:none` 而不補 ring 的情形。

## 1.5 a11y（無障礙）

- **語意**：容器用 `<article>`；標題用真實 heading（`/projects` grid 的卡片建議 `h3`，置於頁面 `h1`/`h2` 之下，維持階層）。
- **標題即可及名稱**：主連結文字 = 專案標題，screen reader 唸得出目的地，不靠 `aria-label` 補。
- **tag 列語意**：用 `<ul>/<li>`；對純展示文字無需額外 ARIA。若 tag 對理解非必要，可考慮 `aria-hidden` 留視覺、不入無障礙樹（預設仍保留，讓 SR 使用者知道技術棧）。
- **cover 圖**：裝飾性封面 `alt=""`（空 alt，從無障礙樹移除，避免冗餘唸圖）；若封面含可辨識資訊才給描述性 `alt`。預設視為裝飾。
- **連結文字明確**：`links` 的 `label` 應自解釋（"View" / "Source"）。同頁多卡會有重複 "View"，建議以 `aria-label`（如 `View {title}`）或視覺隱藏後綴讓每個連結在連結清單中唯一可辨。
- **對比（WCAG AA）**：
  - 描述 `on-surface-muted` `#71717A` on `surface` `#FFFFFF` ≈ 4.5:1（正文門檻，須實測確認 ≥ 4.5:1）。
  - tag `primary` `#2563EB` on `primary-subtle` `#EFF6FF`、link `primary` on `surface`：須實測 ≥ 4.5:1。
  - dark：muted `#A1A1AA` on `surface-dark-subtle` `#18181B`、accent 一律 `primary-bright`，須實測達標。
- **tap target ≥ 44px**：
  - 標題主連結因「整卡可點」覆蓋面遠大於 44px ✔。
  - `links`（View/Source）為小文字連結，須確保可點高度 ≥ 44px（用 `py` 撐高或加大 hit area），且彼此 `gap-md` 避免誤觸。
  - tag 非互動，不受 44px 限制。
- **文字縮放**：支援放大至 200% 不破版（`line-clamp` 仍生效、卡片高度隨之增長，grid 自適應）。
- **reduced-motion**：尊重，hover/focus 過渡可降為無動畫。

## 1.6 「整張卡片是否可點」— 決策與理由（關鍵 a11y 取捨）

**結論：採「標題為唯一主連結 + 偽元素覆蓋整卡」模式（stretched-link / `::after` overlay），不把整卡包成單一 `<a>`。**

理由：
1. **巢狀互動是無效 HTML 且破壞 a11y**：本卡片含多個 `links`（View / Source）。若整卡是一個 `<a>`，把其它 `<a>` 包進去 → `<a>` 巢狀（HTML 不允許），且整卡連結會吞掉內部連結的鍵盤可及性與語意，screen reader 連結清單會塌成一條。
2. **DESIGN.md 範例「整卡為單一連結」是針對無內部連結的卡**；本卡有 Source 等次要連結，須用相容做法達到同樣的「整面可點」體感。
3. **採用的模式**：
   - 標題 `<a>` 為真實主連結（指向專案主要目的地，通常等於 `links` 中的 "View" 或專案詳情）。
   - 該 `<a>` 加 `::after { position:absolute; inset:0 }`，把點擊區「拉伸」覆蓋整卡（容器 `position:relative`）→ 指標使用者點卡片任一空白處都進主連結。
   - tech tag 與 `links`（含 Source）設 `position:relative; z-index:1`，浮在 overlay 之上 → 仍各自可點、可單獨聚焦。
4. **效果對位**：
   - 指標：整卡可點 ✔；hover 整卡 border 變色 ✔。
   - 鍵盤/SR：只有一個主 tab stop（標題）+ 真實次要連結，無重複、無塌陷 ✔。
   - 文字選取：overlay 會略阻礙卡內文字選取——可接受（卡片以導覽為主）；如需選取再評估改用 JS 委派點擊。
5. **避免雙重目的地歧義**：若主連結（標題）指向的 URL 與 `links` 的 "View" 相同，建議**擇一呈現**——標題已是主連結時，`links` 可只保留 "Source" 等次要項，避免「View」與整卡同地兩個入口造成冗餘。此為內容層約定，元件兩種情況都要能正確渲染。

## 1.7 Dark 版（完整對等，accent 一律 `primary-bright`）

| 層 | Light | Dark |
|---|---|---|
| 容器 bg | `surface` `#FFFFFF` | `surface-dark-subtle` `#18181B`（`dark:bg-surface-dark-subtle`） |
| 容器 border | `border` `#E4E4E7` | `border-dark` `#27272A`（`dark:border-border-dark`） |
| 容器 hover border | `primary` | `primary-bright`（`dark:hover:border-primary-bright`） |
| 標題 | `on-surface` | `on-surface-dark`（`dark:text-on-surface-dark`） |
| 描述 | `on-surface-muted` | `on-surface-dark-muted`（`dark:text-on-surface-dark-muted`） |
| cover border | `border` | `border-dark` |
| tag | `bg-primary-subtle` / `text-primary` | **透明填色** + `border` 1px `border-dark` + `text-primary-bright`（DESIGN.md tag dark 規則：`dark:bg-transparent dark:border dark:border-border-dark dark:text-primary-bright`） |
| link | `text-primary` | `text-primary-bright`（`dark:text-primary-bright`），hover 仍 underline |
| focus ring | `primary` | `primary-bright` |

- dark 卡片底用 `surface-dark-subtle`（比頁面 `surface-dark` 高一階），層次靠疊色，不靠陰影。
- dark 不得用 `primary`（對比不足）——所有 accent（border hover / tag 文字 / link / focus）改 `primary-bright`。

---

# Part 2 — 審查 Rubric

> **門檻：總分 ≥ 90 / 100，且所有 [GATE] 必過。** 任一 [GATE] 未過 → 不計分直接退回。最多迭代 **3 輪**。
> **量測以實際渲染為準**：Chrome DevTools computed style（讀 class 不算數，讀算出的像素/色值）、Lighthouse、accessibility tree、screenshot（light + dark 各一）。在 `/projects` grid 與首頁精選兩處各抽查至少一張卡。

## 配分總覽（100 分）

| # | 項目 | 配分 | GATE |
|---|---|---|---|
| 1 | Token 色彩合規 | 14 | |
| 2 | Token 間距合規 | 12 | |
| 3 | Token 字級合規 | 10 | |
| 4 | Token 圓角合規 | 8 | |
| 5 | 版面層次與節奏 | 12 | |
| 6 | 響應式（1→2→3 欄 + 等高） | 10 | |
| 7 | Dark parity | 14 | |
| 8 | 對比 | 8 | **[GATE]** |
| 9 | Console 乾淨 | 4 | **[GATE]** |
| 10 | Focus / 鍵盤 / 整卡可點 a11y | 8 | **[GATE]** |
| | **合計** | **100** | |

---

### 1. Token 色彩合規（14）
- 量測：DevTools 取容器、標題、描述、tag、link 的 computed `color` / `background-color` / `border-color`，逐一比對 DESIGN.md 十六進位。
- 檢查：
  - 容器 bg = `surface` `#FFFFFF`；border = `border` `#E4E4E7`。
  - 標題 = `on-surface` `#0A0A0A`（**標題不得是 link 藍**）。
  - 描述 = `on-surface-muted` `#71717A`。
  - tag bg = `primary-subtle` `#EFF6FF`、text = `primary` `#2563EB`。
  - link text = `primary` `#2563EB`。
  - 全卡無第二色相、無漸層、無 `#000000` 純黑。
- 扣分：每出現一個非 token 色值（含寫死 hex / 近似色）扣 4，扣完為止。

### 2. Token 間距合規（12）
- 量測：DevTools computed `padding` / `gap` / `margin`，比對 4px scale。
- 檢查：
  - 容器 `padding` = 24px（`lg`）四邊一致。
  - 容器內縱向 `gap` = 16px（`md`）。
  - tag 之間 `gap` = 8px（`sm`）。
  - links 之間 `gap` = 16px（`md`）。
  - **不得出現非 scale 值**（如 10px / 18px / 20px 內距）。
- 扣分：每個落在 {4,8,16,24,32,48,64,96} 之外的間距值扣 3。

### 3. Token 字級合規（10）
- 量測：DevTools computed `font-size` / `line-height` / `font-weight` / `letter-spacing`。
- 檢查：
  - 標題 = 20px / 600 / lh 1.3 / -0.01em（`headline-sm`）。
  - 描述 = 16px / 400 / lh 1.7（`body-md`）。
  - tag = 12px / 500 / tracking 0.04em（`label-sm`）。
  - link = 14px / 500（`label-md`）。
  - 字重只出現在 {400,500,600,700}；UI 無第二字體（Inter only，mono 不出現於卡片文字）。
- 扣分：每個不對位的字級 token 扣 3。

### 4. Token 圓角合規（8）
- 量測：DevTools computed `border-radius`。
- 檢查：
  - 容器 = 12px（`lg`）。
  - cover 圖 = 8px（`md`）。
  - tag = 全圓（`full` / 9999px → pill）。
- 扣分：每個不對位圓角扣 3。

### 5. 版面層次與節奏（12）
- 量測：screenshot + DevTools box model。
- 檢查：
  - 視覺順序 cover → 標題 → 描述 → tag → links 清晰、留白充足、不擁擠。
  - 內部只用 `sm`/`md` 兩級節奏，無雜亂間距。
  - 描述 `line-clamp` 生效，不撐爆卡片。
  - 缺欄位（無 cover / 無 tag / 無 links）時不留空佔位、收合乾淨。
  - **flat / border-driven**：computed `box-shadow` 為 `none`（卡片不得有陰影）。
- 扣分：擁擠/節奏亂扣至多 6；出現任何 box-shadow 扣 6。

### 6. 響應式（10）
- 量測：DevTools 改視窗寬（mobile ≈375 / tablet ≈768 / desktop ≈1280），各截圖。
- 檢查：
  - grid 1 → 2 → 3 欄正確切換，欄間 `gap-lg`(24px)。
  - 卡片在窄寬時不縮 padding（仍 24px）、cover 維持 `16/9` 比例不變形。
  - 同列卡片等高、links 列底邊對齊（`h-full` + `mt-auto`）。
  - 文字放大 200% 不破版。
- 扣分：每個斷點問題扣 3。

### 7. Dark parity（14）
- 量測：切 `.dark`，DevTools computed 值 + dark screenshot，逐項比對 1.7 表。
- 檢查：
  - 容器 bg = `surface-dark-subtle` `#18181B`、border = `border-dark` `#27272A`。
  - 標題 `on-surface-dark`、描述 `on-surface-dark-muted`。
  - tag = 透明填色 + `border-dark` 外框 + `primary-bright` 文字（**非沿用 light 的 `primary-subtle`**）。
  - link / hover border / focus ring 全用 `primary-bright`，**dark 中不得出現 `primary` `#2563EB`**。
- 扣分：每個 dark 缺漏或誤用 `primary`（應為 `primary-bright`）扣 4。

### 8. 對比 [GATE]（8）
- 量測：DevTools 對比工具 / Lighthouse a11y / 手動算 computed 前後景色比。
- 門檻（WCAG AA）：正文 ≥ 4.5:1、大字（≥24px 或 ≥18.66px bold）≥ 3:1。
- 檢查（light + dark 皆需過）：
  - 描述 muted 文字 ≥ 4.5:1。
  - tag 文字（on `primary-subtle` / dark on 透明底）≥ 4.5:1。
  - link 文字 ≥ 4.5:1。
  - 標題 ≥ 4.5:1。
  - hover/focus border 對背景可辨。
- **未達標即 GATE fail**（不論其它分數）。

### 9. Console 乾淨 [GATE]（4）
- 量測：DevTools Console + Network，載入 `/projects` 與首頁。
- 門檻：**無 error、無 warning**（含 React hydration warning、缺圖 404、a11y/HTML 驗證警告如巢狀 `<a>`）。
- **任一 error/warning 即 GATE fail。**

### 10. Focus / 鍵盤 / 整卡可點 a11y [GATE]（8）
- 量測：鍵盤 Tab 實測 + accessibility tree + DevTools。
- 門檻（全部須過）：
  - Tab 進卡片：主連結（標題）可聚焦並顯示 2px `primary`/`primary-bright` `:focus-visible` ring（非 glow）。
  - 各 `links`（View/Source）可單獨 Tab 聚焦、各有可見 focus 樣式。
  - tag **不可**被 Tab 聚焦（非互動）。
  - 整卡可點（指標點空白處進主連結）**且**未犧牲內部連結可及性——a11y tree 無巢狀 `<a>`、連結清單每條可辨（無重複塌陷）。
  - 互動連結可點高度 ≥ 44px。
  - cover 裝飾圖 `alt=""`（不入無障礙樹）。
- **任一項未過即 GATE fail。**

---

## 迭代規則
- 每輪：visual-reviewer 用上表評分並列出未過項（含量測值）→ astro-frontend-developer 修 → 重測。
- 通過條件：總分 ≥ 90 **且** 第 8/9/10 三個 [GATE] 全過。
- 最多 3 輪；3 輪未達標則升級回報（列出殘留缺口與量測證據），不放水標記通過。

---

## 附錄 — 提案新增 token（不硬寫進規格）

DESIGN.md 已涵蓋本元件所有色彩/字級/圓角/間距，但有兩個值目前無對應 token，按「先提案、後採用」處理：

1. **封面圖長寬比 `aspect-cover`（建議 `16 / 9`）**
   - 用途：固定 cover 高度，避免 grid 跳動、確保同列卡片等高。
   - 現況：DESIGN.md 無 aspect-ratio token。建議於 DESIGN.md 增列（如 `aspect.cover: 16/9`）後，元件再引用；採納前可暫以 `aspect-[16/9]` 實作並在 PR 標註待 token 化。
2. **互動連結最小 hit area 高度（44px tap target）**
   - 對應 DESIGN.md a11y 規範「tap target ≥ 44px」，數值本身已是規範常數，非新色票/間距 token；以 `min-h-[44px]` 或 `py` 撐高實作即可，不需新增設計 token。

> 上述 1 為真正的「提案新增 token」；2 屬既有 a11y 規範的實作手段，列此僅為透明說明。除這兩點外，本元件 100% 使用既有 token。
