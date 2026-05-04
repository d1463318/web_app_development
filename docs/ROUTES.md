# 路由設計文件 (ROUTES)

## 1. 路由總覽表格

本專案專注於「食譜」的操作，採用標準的 RESTful URL 結構設計。
> 註：由於瀏覽器 HTML 原生表單 `<form>` 在方法上僅保證支援 GET 與 POST，針對更新 (Update) 與刪除 (Delete) 動作，我們於路徑中加上動詞（如 `/edit`, `/delete`），並使用 POST 替代 PUT/DELETE。

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁/全覽 | GET | `/` 或 `/recipes` | `index.html` | 展示系統首頁與所有的食譜卡片/清單 |
| 新增頁面 | GET | `/recipes/new` | `edit.html` | 呈現空白的新增輸入表單 (與編輯共用模板) |
| 送出新增 | POST | `/recipes/new` | — | 接收並驗證新建資料，寫入 DB 後轉跳 |
| 食譜詳情 | GET | `/recipes/<id>` | `detail.html` | 顯示單一食譜的詳細材料與製作步驟 |
| 編輯頁面 | GET | `/recipes/<id>/edit` | `edit.html` | 讀取 DB 資料，於表單內預填好舊內容以供修改 |
| 送出更新 | POST | `/recipes/<id>/edit` | — | 接收新的表單內容，覆寫資料後轉跳回詳情頁 |
| 送出刪除 | POST | `/recipes/<id>/delete` | — | 從 DB 移除該資料，轉跳回首頁 |
| 切換收藏 | POST | `/recipes/<id>/favorite` | — | 切換 is_favorite 狀態，轉跳回原本點擊的網頁 |

---

## 2. 每個路由的詳細說明

### `GET /recipes` (首頁/搜尋結果)
- **輸入**：URL 參數 `?q=<關鍵字>` (可選)。
- **處理邏輯**：呼叫 Model 的 `get_all(search_query)` 判斷有無帶入搜尋邏輯。
- **輸出**：將資料表傳給 `index.html` 進行渲染。

### `GET /recipes/new` (新增表單頁)
- **處理邏輯**：只需負責指派 Jinja 渲染。
- **輸出**：渲染 `edit.html`。可傳入特定變數（如 `action='create'`）來替換按鈕與標題文字。

### `POST /recipes/new` (新增存檔API)
- **輸入**：表單的 `title`, `ingredients`, `steps`。
- **處理邏輯**：驗證有無空白欄位。若成功則呼叫 `RecipeModel.create`。
- **輸出**：轉跳至剛建好的 `/recipes/<new_id>` (HTTP 302)。
- **錯誤處理**：若輸入有誤 (例如空標題)，則附帶錯誤 Flash 訊息重新回傳 `edit.html` 畫面。

### `GET /recipes/<recipe_id>` (單篇詳情)
- **輸入**：路徑動態變數 `<recipe_id>`。
- **處理邏輯**：到資料庫尋找該筆資料 (`RecipeModel.get_by_id`)。
- **輸出**：帶入資料渲染 `detail.html`。
- **錯誤處理**：如果找不到資料，回傳 Flash 報錯並導向首頁。

### `GET /recipes/<recipe_id>/edit` (編輯表單頁)
- **處理邏輯**：根據被觸發的 `id` 取出現有資料。
- **輸出**：渲染 `edit.html`，並把既有資料作為 value 的方式填入 textarea 或 input。

### `POST /recipes/<recipe_id>/edit` (編輯存檔API)
- **處理邏輯**：與新建食譜相似，只是改為執行 `RecipeModel.update` 去 UPDATE 舊有資料。
- **輸出**：編輯成功轉跳回詳情頁 `/recipes/<id>`。

### `POST /recipes/<recipe_id>/delete` (刪除)
- **處理邏輯**：執行 `RecipeModel.delete`。
- **輸出**：重新導向回 `/recipes` 首頁。

### `POST /recipes/<recipe_id>/favorite` (收藏按鈕)
- **處理邏輯**：執行 `RecipeModel.toggle_favorite` 改變資料庫內的收藏狀態值。
- **輸出**：這顆按鈕可能在首頁點擊，也可能在詳情頁點擊，完成後請導回使用者觸發事件前的原始頁面。

---

## 3. Jinja2 模板清單

位於 `app/templates/`。全部模板預計都會繼承 `base.html`，以符合 DRY (Don't Repeat Yourself) 原則：

1. `base.html`：**底層母版**。負責包裝全域 `<html>`, `<head>` (如字體與 CSS)，固定顯示頂層 Navbar 與 Footer。
2. `index.html`：**首頁**。顯示食譜列表 (卡片形式) 及搜尋列。裡面使用 Jinja2 `{% for r in recipes %}`。
3. `detail.html`：**詳情頁**。純展示頁面。具備進入編輯、刪除的點擊按鈕。
4. `edit.html`：**表單頁**。被「建立新食譜」與「更新舊食譜」共用的表單，包含標題輸入框與文字編輯區塊。

---

## 4. 路由骨架程式碼

已創建在 `app/routes/routes.py`。內部將 Flask 的修飾器 (Decorator) 與處理函式的骨架先行寫好，讓後續開發能迅速將 Model 帶進去填寫實作細節。
