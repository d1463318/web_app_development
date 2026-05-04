# 食譜收藏夾 流程圖 (Flowcharts)

本文件將展示食譜收藏夾系統的使用者操作動線（User Flow），以及後端資料處理的系統序列圖（Sequence Diagram），並列出未來將要實作的路由對照表。

---

## 1. 使用者流程圖 (User Flow)

描述使用者進入系統後，可以進行的各種操作路徑及畫面流轉：

```mermaid
flowchart LR
    Start([使用者開啟網站]) --> Home[首頁 - 食譜總列表]
    
    Home --> Action{選擇操作}
    
    %% 新增流程
    Action -->|點擊「新增食譜」| CreateForm[進入新增表單頁]
    CreateForm -->|送出表單| SaveNew[儲存成功，跳轉回首頁或詳情頁]
    
    %% 搜尋與瀏覽流程
    Action -->|輸入搜尋關鍵字| FilterList[重新顯示過濾後的清單]
    Action -->|點選某篇食譜| Detail[進入食譜詳細檢視頁]
    FilterList -->|點選某篇食譜| Detail
    
    %% 收藏切換流程
    Action -->|點擊「收藏按鈕」| ToggleFavList[更新列表上的收藏狀態]
    Detail -->|點擊「收藏按鈕」| ToggleFavDetail[更新詳情頁上的收藏狀態]
    
    %% 編輯與刪除流程
    Detail --> DetailAction{進階操作}
    
    DetailAction -->|點擊「編輯」| EditForm[進入編輯表單頁]
    EditForm -->|儲存變更| Detail
    
    DetailAction -->|點擊「刪除」| ConfirmDelete[跳出確認提示]
    ConfirmDelete -->|確認刪除| DeleteSuccess[刪除成功，跳轉回首頁]
    ConfirmDelete -->|取消| Detail
```

---

## 2. 系統序列圖 (Sequence Diagram)

以**「新增食譜功能」**為例，描述從使用者送出表單到資料庫寫入的完整資料處理流程：

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (前端)
    participant Flask as Flask (控制器)
    participant Model as 模組邏輯 (Model)
    participant DB as SQLite 資料庫

    User->>Browser: 填寫食譜名稱、材料、步驟並點擊【送出】
    Browser->>Flask: 發送 HTTP POST /recipes/new
    Flask->>Flask: 驗證表單資料 (確認欄位非空)
    
    alt 資料驗證成功
        Flask->>Model: 呼叫 create_recipe(data)
        Model->>DB: 執行 SQL: INSERT INTO recipes ...
        DB-->>Model: 回傳成功狀態或新資料 ID
        Model-->>Flask: 確認建立完成
        Flask-->>Browser: HTTP 302 Redirect 重導向至首頁 (或詳情頁)
        Browser-->>User: 畫面更新，看到新建立的食譜
    else 資料驗證失敗
        Flask-->>Browser: HTTP 200 返回原本的表單頁面，並攜帶錯誤訊息
        Browser-->>User: 畫面上顯示紅字提醒 (如：標題不可空白)
    end
```

---

## 3. 功能清單對照表 (Route Map)

在準備進入開發與實作前，我們預先定義出這五大核心功能所對應的 HTTP 方法與路由規則：

| 主要功能 | 網頁操作動作 | HTTP 方法 | URL 路徑 (範例) | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **瀏覽與搜尋** | 顯示列表/搜尋結果 | GET | `/` 或 `/recipes` | 系統首頁，可透過 `?q=關鍵字` 進行搜尋過濾。 |
| **建立食譜** | 顯示建立表單 | GET | `/recipes/new` | 呈現空白的輸入表單頁面。 |
| **建立食譜** | 儲存新的食譜 | POST | `/recipes/new` | 接收表單內容並將資料寫入 SQLite。 |
| **查看食譜** | 顯示單一詳細內容 | GET | `/recipes/<id>` | 針對特定食譜 ID 取得材料與步驟。 |
| **編輯食譜** | 顯示編輯表單 | GET | `/recipes/<id>/edit` | 呈現包含舊資料的表單頁面。 |
| **編輯食譜** | 更新舊有食譜 | POST | `/recipes/<id>/edit` | 接收修改後的內容並更新至 SQLite。 |
| **刪除食譜** | 執行刪除動作 | POST | `/recipes/<id>/delete` | 刪除特定食譜（為防止 CSRF，實務上常以 POST 取代 DELETE）。|
| **收藏食譜** | 切換收藏狀態 | POST | `/recipes/<id>/favorite` | 將該食譜狀態在「已收藏 / 未收藏」間切換。 |
