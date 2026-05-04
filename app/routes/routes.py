from flask import Blueprint, render_template, request, redirect, url_for, flash

# 由於專案較為簡單，我們建立一個統管食譜相關視圖的 Blueprint
# 若未來系統龐大，可將功能拆分成多個 Blueprint
recipes_bp = Blueprint('recipes', __name__)

@recipes_bp.route('/')
@recipes_bp.route('/recipes')
def index():
    """
    顯示所有食譜，包含搜尋結果。
    - GET 參數: q (搜尋關鍵字，可略)
    - 渲染模板: index.html
    """
    pass


@recipes_bp.route('/recipes/new', methods=['GET'])
def create_recipe_form():
    """
    顯示新增食譜表單。
    - 渲染模板: edit.html
    """
    pass


@recipes_bp.route('/recipes/new', methods=['POST'])
def create_recipe():
    """
    接收新增食譜的表單資料並儲存。
    - POST 表單參數: title, ingredients, steps
    - 成功: 導向至 /recipes/<id> 詳情頁
    """
    pass


@recipes_bp.route('/recipes/<int:recipe_id>', methods=['GET'])
def view_recipe(recipe_id):
    """
    顯示特定食譜詳情。
    - 渲染模板: detail.html
    - 找不到食譜時導回首頁或拋出 404
    """
    pass


@recipes_bp.route('/recipes/<int:recipe_id>/edit', methods=['GET'])
def edit_recipe_form(recipe_id):
    """
    顯示特定食譜的編輯表單 (預填現有資料)。
    - 渲染模板: edit.html
    """
    pass


@recipes_bp.route('/recipes/<int:recipe_id>/edit', methods=['POST'])
def update_recipe(recipe_id):
    """
    接收食譜的更新資料並存入 DB。
    - POST 表單參數: title, ingredients, steps
    - 成功: 導向回 /recipes/<id> 詳情頁
    """
    pass


@recipes_bp.route('/recipes/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    """
    刪除特定食譜操作。
    - 成功: 導向回首頁 /recipes
    """
    pass


@recipes_bp.route('/recipes/<int:recipe_id>/favorite', methods=['POST'])
def toggle_favorite(recipe_id):
    """
    切換食譜的收藏狀態 (加入 / 移除)。
    - 成功: 回到請求發送前的頁面
    """
    pass
