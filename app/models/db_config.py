import sqlite3
import os

# 設定 SQLite 資料庫檔案的存放路徑 (指向上層的 instance 目錄中)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'database', 'schema.sql')

def get_db_connection():
    """獲取並回傳資料庫連線"""
    # 確保 instance 資料夾存在，避免啟動時出錯
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    # 將回傳資料轉化類似字典，以 dict 鍵值存取代替陣列索引
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化資料庫 (依照 schema.sql 建立資料表)"""
    # 確保 database 目錄及其 schema.sql 存在且正確被讀取
    if os.path.exists(SCHEMA_PATH):
        with get_db_connection() as conn:
            with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
            conn.commit()
    else:
        print(f"Warning: 找不到 SQL 定義檔 {SCHEMA_PATH}")
