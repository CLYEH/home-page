# Homepage `/` — 規格 + 審查 Rubric

> 設計唯一來源：`/Users/clyeh/home-page/DESIGN.md`。token 程式對應：`src/styles/global.css` 的 `@theme`（Tailwind v4，無 `tailwind.config`）。
> 本檔只用既有 token 名 / 語意化 class，**不寫死色票或魔術數字**。任何 DESIGN.md 未涵蓋的值都以「提案新增 token」處理（見最後一節），不硬寫進規格。
> 重用元件：精選區直接重用 **ProjectCard**（規格見 `docs/specs/project-card.md`），外觀不改、僅用預設 `headingLevel=3`。

---

## 用途與範圍

- 路由 `/`（`src/pages/index.astro`），是站點的門面：Hero → 精選 Projects → 簡短 About → 聯絡。
- 由 `BaseLayout.astro` 包覆，已提供：
  - `<main class="mx-auto w-full max-w-[1120px] px-lg py-2xl md:px-2xl">`（landmark + grid 寬度 ~1120px + 頁面 gutter 24/48px）。
  - 全站 `Nav`（nav landmark + ThemeToggle island）與 `footer`（contentinfo）。
- **因此本頁不重複頁面外距/最大寬，只負責 `<main>` 內各 section 的結構、節奏與 prose 收斂。**
- 互動：**零新增 client JS**。全頁靜態 `.astro`；唯一 island 是既有 ThemeToggle（在 Nav 內，不屬本頁）。

---

# Part 1 — 規格 Spec

## 1.0 頁面骨架與 heading 階層（全頁唯一 h1）

```
main (BaseLayout 提供，max-w-1120 / 置中 / px gutter)
└─ slot = index.astro
   ├─ section[aria-labelledby="hero-title"]        Hero
   │    ├─ h1#hero-title  (姓名)  ← 全頁唯一 h1，headline-display
   │    ├─ p (標語)                body-lg，~720px
   │    └─ div (CTA 列)            button-primary + button-secondary
   ├─ section[aria-labelledby="work-title"]        精選 Projects
   │    ├─ header: h2#work-title (Selected work) + "View all →" link
   │    └─ ul.grid (1→2→3 欄, gap-lg)
   │         └─ li > ProjectCard (headingLevel=3 → 卡片 h3)
   ├─ section[aria-labelledby="about-title"]        簡短 About
   │    ├─ h2#about-title (About)
   │    ├─ p (引言)               body-lg，~720px prose
   │    └─ "More about me →" link
   └─ section[aria-labelledby="contact-title"]      聯絡
        ├─ h2#contact-title (Get in touch)
        └─ nav/ul (email / GitHub … link 列)
```

heading 階層：**h1（Hero 姓名，全頁唯一）→ 每個 section 一個 h2 → ProjectCard 內 h3**。連續、不跳級、不重複 h1。

- 每個 section 都是 `<section aria-labelledby="…">`，`aria-labelledby` 指向該 section 的 heading `id` → 形成具名 landmark region，screen reader 可逐區跳。
- 聯絡 link 列建議包在 `<nav aria-label="Contact">` 內（語意上是一組導向外部聯絡管道的連結）。

## 1.1 區塊節奏（section 之間 / section 內）

全部間距取自 4px scale，不出現中間值。

| 位置 | 間距 token | 值 | 依據 |
|---|---|---|---|
| section ↔ section（主要區塊之間） | `mt-3xl`（建議行動裝置）→ `md:mt-4xl`（桌機） | 64 → 96px | DESIGN.md「major sections 64–96px」；桌機留白更慷慨 |
| Hero 內：h1 ↔ 標語 | `mt-md` | 16px | 標語緊跟標題、同一語義塊 |
| Hero 內：標語 ↔ CTA 列 | `mt-xl` | 32px | 從文字到行動，拉開一階 |
| section header（h2）↔ 內容（grid / prose） | `mt-2xl` | 48px | 標題與其內容是「相關塊」上緣 |
| About：h2 ↔ 引言 | `mt-xl` | 32px | |
| About：引言 ↔ "More about me →" | `mt-lg` | 24px | link 屬引言的延伸動作 |
| Contact：h2 ↔ link 列 | `mt-xl` | 32px | |
| 精選 grid 欄間 / 列間 | `gap-lg` | 24px | DESIGN.md project grid gutter |
| CTA 兩顆按鈕之間 | `gap-md` | 16px | 控制元件之間 |
| Contact link 之間 | `gap-md`（行內）/ `gap-lg`（多行時更鬆） | 16 / 24px | 給足 tap 間距 |

> 第一個 section（Hero）不需頂部 margin——`<main>` 已給 `py-2xl`(48px)。section 之間的節奏用「下一個 section 的 `mt-3xl`/`md:mt-4xl`」表達，避免上下都加造成雙倍。

## 1.2 欄寬與置中

- **grid 寬**：精選 Projects 的 `ul.grid` 滿 `<main>` 寬（~1120px），不再收斂。
- **prose 寬 ~720px**：Hero 標語、About 引言這類連續閱讀文字，外層加 `max-w-prose-token`（提案 token，見末節；採納前暫以 `max-w-[720px]`）。
  - Hero 文字塊靠左對齊、`max-w` 收斂（不置中文字，左對齊更易讀、更像 portfolio）。
  - About 引言同樣 `max-w` 收斂、左對齊。
- **section header / 聯絡**：標題與其輔助 link 在 ~1120px 容器內自然靠左；不需額外置中。
- DESIGN.md「Center within the viewport」由 `<main>` 的 `mx-auto` 達成；本頁不再重複置中容器。

## 1.3 Hero（區塊 1）

| 元素 | token / class | 說明 |
|---|---|---|
| section | `<section aria-labelledby="hero-title">` | landmark；Hero 無頂 margin（`<main>` py 已給） |
| 文字塊容器 | `max-w-[720px]`（提案 `max-w-prose-token`） | prose 寬，左對齊 |
| h1 姓名 | `text-headline-display`(60/700, lh1.05, -0.03em) · `text-on-surface` | **全頁唯一 h1**；DESIGN.md「hero name, one per page」 |
| 標語 `p` | `text-body-lg`(18/400, lh1.7) · `text-on-surface-muted` · `mt-md` | 一句話定位；muted 與 h1 形成層次 |
| CTA 列 `div` | `mt-xl flex flex-wrap items-center gap-md` | 兩顆按鈕並排，窄屏自動換行 |
| CTA 主（button-primary） | `button-primary` token：`bg-primary` · `text-on-primary` · `rounded-md`(8px) · `text-label-md`(14/500) · 高 44px · 左右 padding 對齊 token（`px-[20px]` → 提案 `px-button-token`，見末節） | 文案如 **"View projects"** → `/projects`。**全視圖唯一 primary。** hover → `bg-primary-hover` |
| CTA 次（button-secondary） | `button-secondary` token：`bg-surface` · `border` 1px `border-border` · `text-on-surface` · `rounded-md` · `text-label-md` · 高 44px | 文案如 **"Get in touch"** → 跳到 `#contact`（頁內聯絡 section）或 `mailto:`。hover → `bg-surface-subtle` |

設計理由：

- **一個 primary + 一個 secondary**，落實「每視圖只有一個 primary button」。主要動作是看作品（最符合 portfolio 目的），次要才是聯絡。
- 兩顆都是 44px 高（DESIGN.md button token）→ 滿足 tap target ≥ 44px。
- secondary 用 border 區隔，不靠陰影；與 primary 同高同圓角，視覺成對。
- accent（primary 填色）只出現在這一顆主按鈕 + link，符合「accent 克制、不鋪大面積」。

## 1.4 精選 Projects（區塊 2）

| 元素 | token / class | 說明 |
|---|---|---|
| section | `<section aria-labelledby="work-title" class="mt-3xl md:mt-4xl">` | 與 Hero 拉開 64/96px |
| header `div` | `flex items-baseline justify-between gap-md flex-wrap` | 標題左、"View all →" 右；窄屏換行 |
| h2 標題 | `text-headline-lg`(40/700, lh1.1, -0.02em) · `text-on-surface` · `id="work-title"` | 文案如 **"Selected work"** |
| "View all →" `a` | `link` token：`text-primary` · `text-label-md` · 平時 `no-underline` · hover `underline` | → `/projects`；可點高度 ≥ 44px（`inline-flex min-h-[44px] items-center`） |
| grid `ul` | `mt-2xl grid grid-cols-1 gap-lg sm:grid-cols-2 lg:grid-cols-3` | 與 `/projects` 一致；1→2→3 欄、`gap-lg`(24px) |
| 卡片 `li > ProjectCard` | **重用 ProjectCard，`headingLevel` 用預設 3** | 取 `featured` 為真者；外觀完全不改（見 project-card.md） |

精選資料取法（內容層，非視覺）：

- `getCollection('projects')` filter `data.featured === true`，依 `order` 排序。
- 數量建議 ≤ 3（一列）或 ≤ 6（兩列）以維持首頁克制；實際數量由內容決定，grid 自適應。
- 若無任何 featured：整個精選 section 可不渲染（避免空標題）；此為內容層約定，元件/頁面都要能正確處理空集合。

設計理由：

- 直接重用 ProjectCard → 與 `/projects` 視覺零差異，維持一致性；首頁不另立卡片樣式。
- `headingLevel=3` 是關鍵：首頁 section 標題是 **h2**，卡片必須降一階為 **h3**（`/projects` 因頁面 h1 是 "Projects"、section 標題才用 h2，兩頁情境不同，故傳值不同）。
- "View all →" 用 link（非第二顆 button），守住「一個 primary／視圖」。

## 1.5 簡短 About（區塊 3）

| 元素 | token / class | 說明 |
|---|---|---|
| section | `<section aria-labelledby="about-title" class="mt-3xl md:mt-4xl">` | |
| h2 | `text-headline-lg` · `text-on-surface` · `id="about-title"` | 文案如 **"About"** |
| 引言容器 | `max-w-[720px]`（提案 `max-w-prose-token`）· `mt-xl` | prose 寬，左對齊 |
| 引言 `p` | `text-body-lg`(18/400, lh1.7) · `text-on-surface-muted` | 2–3 句自我介紹；lead copy 用 `body-lg` |
| "More about me →" `a` | `link` token：`text-primary` · `text-label-md` · hover underline · `mt-lg` · 可點高度 ≥ 44px | → `/about` |

設計理由：

- 首頁只放「引言 + 一條 link 到 /about」，不塞完整經歷——克制、留白優先，細節留給 /about。
- 引言用 `body-lg`（lead copy）+ muted 色：是介紹文，不與 h2 爭強度。

## 1.6 聯絡（區塊 4）

| 元素 | token / class | 說明 |
|---|---|---|
| section | `<section aria-labelledby="contact-title" class="mt-3xl md:mt-4xl">` | id 為 Hero secondary CTA `#contact` 的錨點目標 |
| h2 | `text-headline-lg` · `text-on-surface` · `id="contact-title"` | 文案如 **"Get in touch"** |
| link 列容器 | `<nav aria-label="Contact"><ul class="mt-xl flex flex-wrap gap-md">` | 一排聯絡 link |
| 各 link `a` | `link` token：`text-primary` · `text-label-md` · 平時 `no-underline` · hover `underline` · `inline-flex min-h-[44px] items-center` | email 用 `mailto:`、GitHub 等用外部 URL；外部連結 `rel="me noopener"`、`target` 視需求 |

設計理由：

- 聯絡用一排 **link**（非 button）：accent 已由 Hero primary 承擔；此處是次級導向，link 足矣，避免第二顆 primary。
- email 第一順位（最直接的聯絡方式），其後 GitHub 等。
- 每條 link 撐到 44px 高、彼此 `gap-md`，避免行動裝置誤觸。
- 此 section 是頁內聯絡區，**不取代** BaseLayout 的 `footer`（footer 是版權 contentinfo，兩者並存）。

## 1.7 Dark 版（完整對等，accent 一律 `primary-bright`）

| 元素 | Light | Dark |
|---|---|---|
| 頁面底 | `surface` `#FFFFFF`（BaseLayout body） | `surface-dark` `#0A0A0A`（`dark:bg-surface-dark`，BaseLayout 已給） |
| h1 / 各 h2 | `on-surface` `#0A0A0A` | `on-surface-dark` `#FAFAFA`（`dark:text-on-surface-dark`） |
| 標語 / About 引言 | `on-surface-muted` `#71717A` | `on-surface-dark-muted` `#A1A1AA`（`dark:text-on-surface-dark-muted`） |
| CTA 主（primary 填色） | `bg-primary` `#2563EB` / `text-on-primary` | **dark 維持 `bg-primary`**（實心按鈕的填色塊，`on-primary` 白字在 `#2563EB` 上對比足；DESIGN.md 規範「accent on dark surfaces 用 primary-bright」針對的是**線/文字 accent**，非實心 primary 按鈕。實心按鈕兩主題同填色，hover 同為 `primary-hover`） |
| CTA 次（secondary） | `bg-surface` / `border-border` / `text-on-surface` | `dark:bg-surface-dark-subtle`（或保持 `surface-dark` 並靠 border）/ `dark:border-border-dark` / `dark:text-on-surface-dark`；hover `dark:bg-surface-dark-subtle` |
| 所有 link（View all / More about me / 聯絡 / hover underline） | `text-primary` `#2563EB` | `text-primary-bright` `#60A5FA`（`dark:text-primary-bright`），**dark 不得用 `primary`** |
| focus ring（按鈕 + 所有 link） | 2px `primary` | 2px `primary-bright`（`dark:focus-visible:outline-primary-bright`） |
| 精選卡片 | 見 project-card.md（dark：`surface-dark-subtle` 底 / `border-dark` / accent `primary-bright`） | 同左，由 ProjectCard 自帶 |

**dark 關鍵取捨（須一致執行）**：

- **line/text accent**（所有 link、focus ring、卡片 hover border）→ dark 一律 `primary-bright`。
- **solid primary 按鈕填色** → 兩主題都用 `bg-primary` + `on-primary` 白字（這是「在 accent 上」而非「accent 在 dark surface 上」，白字 on `#2563EB` 對比達標；若改用 `primary-bright` 填色，白字對比反而不足）。此與 DESIGN.md button-primary token 一致（token 未對 dark 另開填色）。
- dark 層次靠 `surface-dark` → `surface-dark-subtle` 疊色與 1px `border-dark`，**不加陰影**。

## 1.8 a11y（無障礙）

- **landmark**：`<main>`（BaseLayout）內每個 section 為 `<section aria-labelledby>`；聯絡 link 列再包 `<nav aria-label="Contact">`。nav / contentinfo 由 BaseLayout 提供。
- **heading 階層**：h1（唯一）→ section h2 ×4 → 卡片 h3；用 axe / accessibility tree 驗 heading-order 無跳級、無重複 h1。
- **CTA / link focus**：所有按鈕與 link 用 `:focus-visible`，2px ring，light `primary` / dark `primary-bright`，**非 glow**（`focus-visible:outline-2 focus-visible:outline-offset-2`）。
- **tap target ≥ 44px**：兩顆 CTA 高 44px（button token）；所有文字 link（View all / More about me / 聯絡）用 `inline-flex min-h-[44px] items-center` 撐高，彼此 `gap-md` 防誤觸。
- **連結文字明確**：CTA 與 link 文案自解釋（"View projects" / "Get in touch" / "View all" / "More about me" / "Email" / "GitHub"）。"View all →" 的箭頭為視覺裝飾，置於文字後即可（screen reader 唸出 "View all →" 可接受；如需更乾淨可把 "→" 用 `aria-hidden`）。
- **錨點 CTA**：Hero secondary "Get in touch" 指向 `#contact` 時，目標 section 有 `id` 對應；尊重 `prefers-reduced-motion`（平滑捲動須在 reduce 時關閉，建議不強加 `scroll-behavior:smooth` 或以 media query 包覆）。
- **對比（WCAG AA，light + dark 皆需過、以實測為準）**：
  - h1 / h2（大字 ≥24px 或 18.66px bold）≥ 3:1；正文/muted/link ≥ 4.5:1。
  - 標語、About 引言 muted（`#71717A` on `#FFFFFF` ≈ 4.5:1；dark `#A1A1AA` on `#0A0A0A`）須實測達標。
  - link `primary` on `surface` / `primary-bright` on `surface-dark` 須實測 ≥ 4.5:1。
  - button-primary：`on-primary` 白字 on `primary` `#2563EB` 須 ≥ 4.5:1。
- **文字縮放 200%**：所有區塊用 flow + flex-wrap，放大不破版（CTA 列、聯絡列、grid 皆自動換行/重排）。
- **reduced-motion**：hover/focus 過渡與任何平滑捲動在 reduce 時降為無動畫。
- **圖片**：首頁本身無裝飾插圖；精選卡片封面由 ProjectCard 處理（裝飾 `alt=""`）。

## 1.9 近零 JS（DESIGN.md「work is the hero、起始 JS ~0KB」）

- 全頁為靜態 `.astro`；**不新增任何 client island / `client:*` 指令**。
- 唯一 hydrate 的元件是既有 **ThemeToggle**（位於 Nav，非本頁範圍）。
- CTA、link、錨點捲動皆用原生 HTML（`<a href>`），無需 JS。

---

# Part 2 — 審查 Rubric

> **門檻：總分 ≥ 90 / 100，且所有 [GATE] 必過。** 任一 [GATE] 未過 → 不計分直接退回。最多迭代 **3 輪**。
> **量測以實際渲染為準**：Chrome DevTools computed style（讀 class 不算數，讀算出的像素/色值）、Lighthouse / axe、accessibility tree、screenshot（light + dark 各一）、Network/Coverage（JS 量）。在 `/` 路由量測；精選卡片本身的細項以 project-card.md rubric 為準，本 rubric 只查「首頁有無正確重用、heading 階層、節奏」。

## 配分總覽（100 分）

| # | 項目 | 配分 | GATE |
|---|---|---|---|
| 1 | Token 色彩合規 | 12 | |
| 2 | Token 間距合規（區塊節奏） | 14 | |
| 3 | Token 字級合規 | 10 | |
| 4 | Token 圓角合規（CTA） | 6 | |
| 5 | 版面層次與留白（flat/border-driven、prose/grid 寬） | 12 | |
| 6 | 單一 primary / 單一 accent | 8 | |
| 7 | 響應式（CTA/grid/聯絡列 + 200% 縮放） | 8 | |
| 8 | Dark parity | 10 | |
| 9 | Heading 階層連續性 | 6 | **[GATE]** |
| 10 | 對比 | 6 | **[GATE]** |
| 11 | Console 乾淨 | 4 | **[GATE]** |
| 12 | Focus / 鍵盤 a11y | 4 | **[GATE]** |
| 13 | 近零 JS（無新 island） | — | **[GATE]**（不計分，純門檻） |
| | **合計** | **100** | |

---

### 1. Token 色彩合規（12）
- 量測：DevTools 取 h1、h2、標語、引言、CTA 主/次、各 link 的 computed `color` / `background-color` / `border-color`，比對 DESIGN.md hex。
- 檢查：
  - h1 / h2 = `on-surface` `#0A0A0A`（dark `on-surface-dark` `#FAFAFA`）。
  - 標語 / 引言 = `on-surface-muted` `#71717A`（dark `#A1A1AA`）。
  - CTA 主 = `bg-primary` `#2563EB` / 白字 `on-primary`；hover `#1D4ED8`。
  - CTA 次 = `bg-surface` + `border` `#E4E4E7` + `on-surface` 文字。
  - 所有 link = `primary` `#2563EB`（dark `primary-bright` `#60A5FA`）。
  - 全頁無第二色相、無漸層填色、無 `#000000` 純黑。
- 扣分：每出現一個非 token 色值（寫死 hex / 近似色 / 漸層）扣 4，扣完為止。

### 2. Token 間距合規 — 區塊節奏（14）
- 量測：DevTools computed `margin` / `gap` / `padding`，比對 4px scale {4,8,16,24,32,48,64,96}。
- 檢查（對照 1.1 表）：
  - section ↔ section = 64px（mobile）/ 96px（desktop）（`mt-3xl` / `md:mt-4xl`）。
  - Hero：h1↔標語 16px、標語↔CTA 32px。
  - section header↔內容 48px（`mt-2xl`）。
  - About：h2↔引言 32px、引言↔link 24px。Contact：h2↔link 32px。
  - grid `gap` = 24px；CTA 間 16px；聯絡 link 間 16px（或 24px）。
  - **不得出現非 scale 值**（10/18/20/56…）。
- 扣分：每個落在 scale 之外或不符節奏的間距扣 3。

### 3. Token 字級合規（10）
- 量測：DevTools computed `font-size` / `line-height` / `font-weight` / `letter-spacing`。
- 檢查：
  - h1 = 60 / 700 / lh1.05 / -0.03em（`headline-display`）。
  - 各 h2 = 40 / 700 / lh1.1 / -0.02em（`headline-lg`）。
  - 標語 / 引言 = 18 / 400 / lh1.7（`body-lg`）。
  - CTA 文字 / link = 14 / 500（`label-md`）。
  - 字重只出現在 {400,500,600,700}；全頁 Inter（無 mono，首頁無 code）。
- 扣分：每個不對位字級扣 3。

### 4. Token 圓角合規 — CTA（6）
- 量測：DevTools computed `border-radius`。
- 檢查：兩顆 CTA = 8px（`md`）。卡片圓角由 ProjectCard 負責（不在此重複）。
- 扣分：每個不對位圓角扣 3。

### 5. 版面層次與留白（12）
- 量測：screenshot（light + dark, mobile + desktop）+ DevTools box model。
- 檢查：
  - 視覺順序 Hero → Selected work → About → Contact 清晰、留白慷慨、不擁擠。
  - prose 文字塊（標語 / 引言）寬度 ~720px（實測 ≤ ~720px 收斂），grid 滿 ~1120px。
  - **flat / border-driven**：全頁 computed `box-shadow` 為 `none`（CTA、section、容器皆無裝飾陰影）；無 glow / gradient / glassmorphism。
  - secondary CTA 與背景靠 1px border 區隔。
- 扣分：擁擠/節奏亂扣至多 6；出現任何裝飾 box-shadow / gradient / glow 扣 6。

### 6. 單一 primary / 單一 accent（8）
- 量測：screenshot + 清點。
- 檢查：
  - 全頁**只有一顆 button-primary**（Hero 主 CTA）；其餘全為 secondary button 或 link。
  - accent（藍）只出現在：該主按鈕填色 + link 文字 + focus/卡片 hover border；**未鋪大面積、未出現第二色相**。
  - "View all" / "More about me" / 聯絡皆為 link（非第二顆 primary）。
- 扣分：出現第二顆 primary 扣 5；出現第二色相扣 5；accent 鋪大面積填色扣 3。

### 7. 響應式 + 文字縮放（8）
- 量測：DevTools 改視窗寬（≈375 / 768 / 1280）各截圖；瀏覽器字級放大 200%。
- 檢查：
  - 精選 grid 1→2→3 欄正確切換、`gap-lg`(24px)。
  - CTA 列、聯絡 link 列在窄屏 `flex-wrap` 換行不溢出。
  - 桌機 section 間距 96px、行動 64px（節奏隨斷點）。
  - 200% 縮放不破版、不水平捲動、文字不被裁切。
- 扣分：每個斷點/縮放問題扣 2。

### 8. Dark parity（10）
- 量測：切 `.dark`，DevTools computed 值 + dark screenshot，逐項比對 1.7 表。
- 檢查：
  - 頁面底 `surface-dark` `#0A0A0A`；h1/h2 `on-surface-dark`；標語/引言 `on-surface-dark-muted`。
  - **所有 link / focus ring / 卡片 hover border 用 `primary-bright` `#60A5FA`，dark 中不得出現 `primary` `#2563EB` 作為線/文字 accent。**
  - CTA 主在 dark 維持 `bg-primary` 實心填色 + 白字（這是刻意取捨，非缺漏；見 1.7）。
  - CTA 次在 dark 用 `surface-dark` / `surface-dark-subtle` + `border-dark` + `on-surface-dark`。
  - 精選卡片 dark 正確（底 `surface-dark-subtle`、accent `primary-bright`）。
- 扣分：每個 dark 缺漏，或把線/文字 accent 誤用 `primary`（應 `primary-bright`）扣 3。

### 9. Heading 階層連續性 [GATE]（6）
- 量測：accessibility tree / axe heading-order / DevTools Elements。
- 門檻（全部須過）：
  - 全頁**恰好一個 h1**（Hero 姓名）。
  - 4 個 section 各一個 h2（Selected work / About / Get in touch + 精選 header）。
  - 精選卡片標題為 **h3**（ProjectCard `headingLevel=3`），不是 h2、不是 h4。
  - 階層連續 h1→h2→h3，**無跳級**（不出現 h1 後直接 h3、或漏 h2）。
  - 每個 section 有 `aria-labelledby` 指向其 heading id。
- **任一項未過即 GATE fail。**

### 10. 對比 [GATE]（6）
- 量測：DevTools 對比工具 / Lighthouse·axe / 手動算 computed 前後景比。light + dark 皆需過。
- 門檻（WCAG AA）：大字（h1/h2 ≥24px 或 ≥18.66px bold）≥ 3:1；正文/muted/link ≥ 4.5:1。
- 檢查：
  - 標語 / About 引言 muted 文字 ≥ 4.5:1（light + dark）。
  - 所有 link 文字 ≥ 4.5:1（light `primary` / dark `primary-bright`）。
  - button-primary 白字 on `#2563EB` ≥ 4.5:1。
  - h1 / h2 ≥ 3:1（兩主題）。
- **未達標即 GATE fail。**

### 11. Console 乾淨 [GATE]（4）
- 量測：DevTools Console + Network，載入 `/`（light + dark 各切一次）。
- 門檻：**無 error、無 warning**（含 hydration warning、404、HTML 驗證如巢狀 `<a>`、a11y 警告）。
- **任一 error/warning 即 GATE fail。**

### 12. Focus / 鍵盤 a11y [GATE]（4）
- 量測：鍵盤 Tab 實測 + accessibility tree。
- 門檻（全部須過）：
  - Tab 依序經過：（Nav 內元素）→ Hero 主 CTA → Hero 次 CTA → "View all" → 各卡片連結 → "More about me" → 各聯絡 link，順序合理。
  - 每個可聚焦元素顯示 2px `primary`/`primary-bright` `:focus-visible` ring（非 glow、非 `outline:none` 未補）。
  - 互動元素可點高度 ≥ 44px（兩顆 CTA + 所有文字 link）。
  - "Get in touch" 錨點（若指向 `#contact`）能正確定位到 Contact section。
- **任一項未過即 GATE fail。**

### 13. 近零 JS [GATE]（不計分，純門檻）
- 量測：DevTools Network / Coverage / 檢視輸出 HTML 的 `<script>`，比對 build 產物。
- 門檻：
  - 首頁**未新增任何 client island**（無新增 `client:load/idle/visible` 等）。
  - 頁面上的 JS 僅來自既有 ThemeToggle island + BaseLayout 的 no-flash inline 主題腳本。
  - CTA / link / 錨點皆原生 `<a href>`，無為導覽而加的 JS。
- **出現任何本頁新增的 client JS 即 GATE fail。**

---

## 迭代規則
- 每輪：visual-reviewer 用上表評分並列出未過項（含量測值）→ astro-frontend-developer 修 → 重測。
- 通過條件：總分 ≥ 90 **且** 第 9/10/11/12/13 五個 [GATE] 全過。
- 最多 3 輪；3 輪未達標則升級回報（列出殘留缺口與量測證據），不放水標記通過。

---

## 附錄 — 提案新增 token（不硬寫進規格）

DESIGN.md 已涵蓋本頁絕大多數色彩/字級/圓角/間距。以下值目前無直接 token 對應，按「先提案、後採用」處理；採納前以註明的暫用值實作並在 PR 標註待 token 化。

1. **prose 最大寬 `max-w-prose-token`（建議 `720px`）**
   - 用途：Hero 標語、About 引言的閱讀欄寬，落實 DESIGN.md「prose ~720px」。
   - 現況：DESIGN.md Layout 段明定 ~720px，但無對應 Tailwind token（`@theme` 目前無 `--max-w-*`）。建議於 `global.css` `@theme` 增 `--width-prose: 720px`（或等價）後改用語意化 class；採納前暫用 `max-w-[720px]` 並標註。
   - 註：grid 寬 ~1120px 已由 `BaseLayout` 的 `max-w-[1120px]` 提供，無須新 token。

2. **button 水平 padding（`20px`，DESIGN.md button token `padding: 20px`）**
   - 用途：button-primary / button-secondary 左右內距。
   - 現況：值已是 DESIGN.md `components.button-*.padding`(20px) 的規範常數，但 20px 不在 spacing scale {…16,24…} 內，故無語意化 spacing class。建議於 `@theme` 增 `--spacing-button-x: 20px`（或於 button 元件統一封裝）後引用；採納前暫以 `px-[20px]` 實作並標註，**因其源自既有 button token、非自創魔術數字**。
   - 註：若已有共用 `Button.astro` / button 樣式封裝此 padding，直接沿用，本頁不重複定義。

> 上述兩項皆源自 DESIGN.md 既有規範（prose 720px、button padding 20px），僅是缺 Tailwind token 對應；屬「補 token 對應」而非自創新值。除此之外，本頁 100% 使用既有 token。
