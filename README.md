# 欽天監｜今日天時 MVP (Qin Tian Jian - 今日天時)

天地運行的今日天時狀態觀測系統。

看見今天天地正在發生什麼。

---

## 1. 核心定位
本系統並非傳統的「吉凶黃曆」或「預言占卜」工具，而是一個天地運行背景動能的觀測系統。
*   **首頁即今日天時**：用戶進入網站即可直接閱讀今日的天時一句話、主題關鍵字、八維語義能量向量與天地人觀察，無須預先輸入任何問題。
*   **非吉凶化**：以八維度語義狀態向量（生成、擴張、穩定、流動、收斂、轉換、瓦解、不確定）展示大氣結構，不給出「大吉/大凶」等命定性結論。
*   **問事為附屬功能**：底部附帶「用今日天時看一件事」API/表單，提供行動的氣場關聯度與節奏建議。

---

## 2. 技術架構
*   **後端框架**：FastAPI (Python)
*   **模板引擎**：Jinja2 (HTML5)
*   **曆法底層**：lunar-python (天干地支、值神、二十八宿、納音)
*   **資料儲存**：SQLite (daily_states 表)
*   **前端樣式**：Vanilla CSS (深墨藍 & 暖金點綴，手機優先響應式排版)

---

## 3. 目錄結構
```
daily_mvp/
├── app.py                     # FastAPI 主程式與 API 端口
├── requirements.txt           # 依賴模組
├── database.py                # SQLite 資料庫與回饋表
├── schemas.py                 # Pydantic 資料結構校驗
├── timing_calculator.py       # 曆法計算業務邏輯
├── semantic_state_engine.py   # 八維語義向量計算
├── daily_interpretation.py    # 文本模板與去重多重語氣
├── content_deduplication.py   # 最近 14 天文字相似度檢測 (Jaccard)
├── social_content_generator.py # 生成 250-450 字 FB/IG 貼文
├── short_message_generator.py # 生成 120-180 字簡短貼文 (LINE/TG)
├── share_card_generator.py    # 調用 Chrome Headless 輸出 1080x1350 PNG
├── feedback_summary.py        # 聚合生成反饋統計與觀察 Markdown
├── daily_publish_pipeline.py  # 整體每日發佈與存檔管線主程式
├── templates/                 # 模板檔
│   ├── today.html             # 今日天時首頁 (分層 UI + 反饋)
│   ├── date.html              # 指定日期結果頁 (分層 UI + 反饋)
│   ├── archive.html           # 歷史檔案清單頁
│   └── share_card.html        # 分享卡 HTML 視覺模板
├── static/                    # 靜態資源
│   ├── style.css              # 欽天監高留白視覺美學 (含折疊 UI)
│   └── app.js                 # 查詢、問事、反饋提交邏輯
├── daily_outputs/             # 存放每日自動生成之 Package 存檔
└── tests/                     # 單元測試
    ├── test_timing_calculator.py
    ├── test_semantic_state_engine.py
    ├── test_daily_generation.py
    ├── test_content_deduplication.py
    ├── test_feedback_api.py
    └── test_daily_publish_pipeline.py
```

---

## 4. 啟動與執行

### 安裝依賴
```bash
pip install -r requirements.txt
```

### 每日排程管線執行 (定時任務)
```bash
# 計算、去重、渲染、截圖，並在 daily_outputs/ 下存檔 Package
python daily_publish_pipeline.py --date 2026-07-16
```

### 生成反饋統計摘要 (CLI)
```bash
# 輸出比率與文字觀察至 feedback_summary_7d.md
python feedback_summary.py --days 7
```

### 啟動本地網頁伺服器
```bash
uvicorn app:app --reload
```
訪問網址：`http://127.0.0.1:8000`

---

## 5. 運行單元測試
可使用 venv 環境下之 python 逐個執行單元測試：
```bash
python tests/test_timing_calculator.py
python tests/test_semantic_state_engine.py
python tests/test_daily_generation.py
python tests/test_content_deduplication.py
python tests/test_feedback_api.py
python tests/test_daily_publish_pipeline.py
```
