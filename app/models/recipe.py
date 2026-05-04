from .db_config import get_db_connection

class RecipeModel:
    @staticmethod
    def create(title, ingredients, steps):
        """新增食譜"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO recipes (title, ingredients, steps) VALUES (?, ?, ?)",
                (title, ingredients, steps)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all(search_query=None):
        """取得食譜列表，若有搜尋關鍵字則過濾，排序優先看『是否收藏』接『最新建立』"""
        with get_db_connection() as conn:
            if search_query:
                query = f"%{search_query}%"
                rows = conn.execute(
                    "SELECT * FROM recipes WHERE title LIKE ? OR ingredients LIKE ? ORDER BY is_favorite DESC, created_at DESC", 
                    (query, query)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM recipes ORDER BY is_favorite DESC, created_at DESC"
                ).fetchall()
            return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(recipe_id):
        """取得單一食譜的詳細資訊"""
        with get_db_connection() as conn:
            row = conn.execute(
                "SELECT * FROM recipes WHERE id = ?", 
                (recipe_id,)
            ).fetchone()
            return dict(row) if row else None

    @staticmethod
    def update(recipe_id, title, ingredients, steps):
        """更新已存在的食譜"""
        with get_db_connection() as conn:
            conn.execute(
                "UPDATE recipes SET title = ?, ingredients = ?, steps = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (title, ingredients, steps, recipe_id)
            )
            conn.commit()
            return True

    @staticmethod
    def toggle_favorite(recipe_id):
        """切換食譜的收藏狀態 (0 <-> 1)"""
        with get_db_connection() as conn:
            # 先獲取當下狀態
            row = conn.execute("SELECT is_favorite FROM recipes WHERE id = ?", (recipe_id,)).fetchone()
            if row:
                new_status = 0 if row['is_favorite'] == 1 else 1
                conn.execute(
                    "UPDATE recipes SET is_favorite = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (new_status, recipe_id)
                )
                conn.commit()
                return new_status
        return None

    @staticmethod
    def delete(recipe_id):
        """刪除食譜"""
        with get_db_connection() as conn:
            conn.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
            conn.commit()
            return True
