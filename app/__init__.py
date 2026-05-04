import os
from flask import Flask
from dotenv import load_dotenv

# 引入已建置的初始化函式與 Blueprint
from .models.db_config import init_db
from .routes.routes import recipes_bp

def create_app():
    # 載入 .env 變數 (如有)
    load_dotenv()
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-dev-secret-key')

    # 因為是 monolithic 架構，註冊前先確保 DB 及表單正確建立
    with app.app_context():
        init_db()

    # 註冊食譜專用的路由 Blueprint
    app.register_blueprint(recipes_bp)

    return app
