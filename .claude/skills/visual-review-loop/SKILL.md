---
name: visual-review-loop
description: 渲染審查迭代 loop：起 dev server，visual-reviewer 用 Chrome DevTools 對 rubric 評分，未達門檻就讓 astro-frontend-developer 修正，反覆迭代到分數過門檻。Use when QA'ing/hardening an implemented component against its design rubric（如「審查 projects 頁」「跑 review loop」「讓它達標」）。
---

# Visual Review Loop（渲染審查迭代）

讓前端產物對著 rubric 反覆修到達標：**起 dev server → `visual-reviewer` 用 Chrome DevTools 評分 → 未達門檻把缺失丟回 `astro-frontend-developer` 修 → 重評**，直到分數過門檻或用盡迭代。

## 何時用
已有實作（通常剛跑完 `/design-to-build`）要做視覺/品質把關。若還沒做出東西，先用 `/design-to-build`。

## 輸入
- 目標 **route**（如 `/projects`）或元件所在頁。
- 對應的 **`docs/specs/<name>.md`**（含 Rubric）。
- **若找不到 rubric**：先用 Agent 叫 `ui-designer` 對該元件補一份規格＋rubric（或請使用者改跑 `/design-to-build`）。**不要無 rubric 硬評**——沒有標準就沒有客觀分數。

## 流程

### 0. 起 dev server
背景執行 `npm run dev`，取得本機 URL（Astro 預設 `http://localhost:4321`）。確認目標 route 可達再往下。

### 1. 評分（agent：`visual-reviewer`）
用 Agent 啟動 `visual-reviewer`，給它 **URL + rubric 檔路徑**。它用 Chrome DevTools 量測，回傳契約格式：
```
SCORE / GATES / RESULT / DEFECTS
```
**保持同一個 visual-reviewer 實例跨輪複用**（瀏覽器分頁不關，HMR reload 後重量測即可）。

### 2. 判定
- `RESULT=PASS`（`SCORE ≥ 門檻` 且所有 `[GATE]` 過）→ 進 5（成功收尾）。
- 否則 → 進 3。

### 3. 修正（agent：`astro-frontend-developer`）
把這輪的 `DEFECTS` 透過 **SendMessage 丟回同一個 `astro-frontend-developer` 實例**（保留它的 code context），要它**逐條**修正。Astro HMR 會自動 reload，不必重啟 server。
- 若這是 loop 的第一輪、FE agent 尚未存在（例如使用者直接跑本 skill），先用 Agent 啟動一個並附上 `docs/specs/<name>.md` 與目前程式碼位置。

### 4. 重評
回到步驟 1，用同一個 visual-reviewer 重新評分。記錄每輪 `SCORE`，方便看是否在進步。

### 5. 收尾
- **達標** → 回報最終 `SCORE`、通過項、各斷點截圖；指出改了哪些檔案。
- **用盡迭代仍未達標** → **據實回報**（fail loud）：最終分數、剩餘 `DEFECTS`、卡關根因（例如 token 沒對應進 `tailwind.config`），不可宣稱成功。
- 關掉背景 dev server。

## 控制參數
- **門檻**：預設 `SCORE ≥ 90/100` 且所有 `[GATE]` 通過。以 rubric 檔內的設定為準；使用者可在呼叫時覆寫。
- **最多迭代**：預設 **3 輪**。達上限即停並照「未達標」收尾。
- **每輪一定要有進展**：若連續兩輪分數無提升且非因 gate 卡死，停下來回報根因，別空轉燒迭代。

## Rubric 評分契約（visual-reviewer 與本 loop 共用）
量測來源（一律以實際渲染為準）：
- `evaluate_script` + `getComputedStyle` → token 對齊（色彩/間距/字級/圓角）。
- `lighthouse_audit` → a11y / performance。
- `take_snapshot` + `take_screenshot` → 結構、focus、層次、版面。
- `list_console_messages` → console 乾淨（[GATE]）。
- `list_network_requests` → JS payload 量。
- `resize_page` → 響應式（mobile/tablet/desktop）。
- 切換 dark（toggle 或對 `<html>` 加 `dark` class）→ dark parity（accent 應為 `primary-bright`）。

visual-reviewer 回傳格式（本 loop 用它判定 PASS/FAIL）：
```
SCORE: <n>/100
GATES: contrast=PASS|FAIL; console=PASS|FAIL; focus=PASS|FAIL; <其他>=PASS|FAIL
RESULT: PASS | FAIL
DEFECTS:
1. [類別][-X分] 觀察到 <實際值> → 期望 <token/規格值> → 建議：<怎麼改>（<檔案:class/選擇器>）
2. ...
NOTES: <rubric 未涵蓋的觀察或疑點>
```

## 角色邊界
- `visual-reviewer`：只量測、評分、列缺失，**對 source code 唯讀**。
- `astro-frontend-developer`：只依缺失改 code，不自評分數。
- 本 skill（orchestrator）：管 dev server 生命週期、跑迴圈、在兩個 agent 間傳遞訊息、判定門檻與收尾。
