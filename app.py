from app import create_app

# 產生全域 app 實例
app = create_app()

if __name__ == '__main__':
    # 啟動開發伺服器
    app.run(host='127.0.0.1', port=5000, debug=True)
