from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.recipe import RecipeModel

# 建立名為 recipes 的 Blueprint
recipes_bp = Blueprint('recipes', __name__)

@recipes_bp.route('/')
@recipes_bp.route('/recipes')
def index():
    """
    顯示所有食譜，包含搜尋結果。
    """
    query = request.args.get('q', '').strip()
    recipes = RecipeModel.get_all(query if query else None)
    return render_template('index.html', recipes=recipes, search_query=query)


@recipes_bp.route('/recipes/new', methods=['GET'])
def create_recipe_form():
    """
    顯示新增食譜表單。
    """
    return render_template('edit.html', action='create', recipe={})


@recipes_bp.route('/recipes/new', methods=['POST'])
def create_recipe():
    """
    接收新增食譜的表單資料並儲存。
    """
    title = request.form.get('title', '').strip()
    ingredients = request.form.get('ingredients', '').strip()
    steps = request.form.get('steps', '').strip()

    # 基本輸入驗證
    if not title or not ingredients or not steps:
        flash('標題、材料與步驟皆為必填欄位！', 'danger')
        return render_template('edit.html', action='create', recipe={
            'title': title,
            'ingredients': ingredients,
            'steps': steps
        })

    data = {'title': title, 'ingredients': ingredients, 'steps': steps}
    new_id = RecipeModel.create(data)

    if new_id:
        flash('食譜新增成功！', 'success')
        return redirect(url_for('recipes.view_recipe', recipe_id=new_id))
    else:
        flash('新增失敗，發生資料庫錯誤。', 'danger')
        return render_template('edit.html', action='create', recipe=data)


@recipes_bp.route('/recipes/<int:recipe_id>', methods=['GET'])
def view_recipe(recipe_id):
    """
    顯示特定食譜詳情。
    """
    recipe = RecipeModel.get_by_id(recipe_id)
    if not recipe:
        flash('找不到該食譜！', 'danger')
        return redirect(url_for('recipes.index'))
    return render_template('detail.html', recipe=recipe)


@recipes_bp.route('/recipes/<int:recipe_id>/edit', methods=['GET'])
def edit_recipe_form(recipe_id):
    """
    顯示特定食譜的編輯表單 (預填現有資料)。
    """
    recipe = RecipeModel.get_by_id(recipe_id)
    if not recipe:
        flash('找不到該食譜！', 'danger')
        return redirect(url_for('recipes.index'))
    return render_template('edit.html', action='edit', recipe=recipe)


@recipes_bp.route('/recipes/<int:recipe_id>/edit', methods=['POST'])
def update_recipe(recipe_id):
    """
    接收食譜的更新資料並存入 DB。
    """
    recipe = RecipeModel.get_by_id(recipe_id)
    if not recipe:
        flash('找不到該食譜！', 'danger')
        return redirect(url_for('recipes.index'))

    title = request.form.get('title', '').strip()
    ingredients = request.form.get('ingredients', '').strip()
    steps = request.form.get('steps', '').strip()

    if not title or not ingredients or not steps:
        flash('標題、材料與步驟皆為必填欄位！', 'danger')
        # 把使用者剛輸入的資料再塞回去，避免剛打字消失
        recipe.update({'title': title, 'ingredients': ingredients, 'steps': steps})
        return render_template('edit.html', action='edit', recipe=recipe)

    data = {'title': title, 'ingredients': ingredients, 'steps': steps}
    if RecipeModel.update(recipe_id, data):
        flash('食譜更新成功！', 'success')
        return redirect(url_for('recipes.view_recipe', recipe_id=recipe_id))
    else:
        flash('更新失敗，發生資料庫錯誤。', 'danger')
        recipe.update(data)
        return render_template('edit.html', action='edit', recipe=recipe)


@recipes_bp.route('/recipes/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    """
    刪除特定食譜操作。
    """
    if RecipeModel.delete(recipe_id):
        flash('食譜已刪除成功！', 'success')
    else:
        flash('刪除失敗。', 'danger')
    return redirect(url_for('recipes.index'))


@recipes_bp.route('/recipes/<int:recipe_id>/favorite', methods=['POST'])
def toggle_favorite(recipe_id):
    """
    切換食譜的收藏狀態 (加入 / 移除)。
    """
    RecipeModel.toggle_favorite(recipe_id)
    # 若請求中帶有上一頁資訊，切換完導回原頁面，否則導回首頁
    next_page = request.headers.get('Referer')
    return redirect(next_page or url_for('recipes.index'))
