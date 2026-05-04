from .db_config import get_db_connection
import sqlite3

class RecipeModel:
    @staticmethod
    def create(data):
        """
        新增筆食譜紀錄
        :param data: dict，包含 title, ingredients, steps
        :return: int (新資料的 id) 或 None (失敗)
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO recipes (title, ingredients, steps) VALUES (?, ?, ?)",
                    (data.get('title'), data.get('ingredients'), data.get('steps'))
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error in create: {e}")
            return None
        except Exception as e:
            print(f"Exception in create: {e}")
            return None

    @staticmethod
    def get_all(search_query=None):
        """
        取得所有食譜記錄
        :param search_query: str，選項式搜尋條件
        :return: list of dicts
        """
        try:
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
        except sqlite3.Error as e:
            print(f"Database error in get_all: {e}")
            return []
        except Exception as e:
            print(f"Exception in get_all: {e}")
            return []

    @staticmethod
    def get_by_id(recipe_id):
        """
        取得單筆歷史紀錄
        :param recipe_id: int
        :return: dict 或 None
        """
        try:
            with get_db_connection() as conn:
                row = conn.execute(
                    "SELECT * FROM recipes WHERE id = ?", 
                    (recipe_id,)
                ).fetchone()
                return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Database error in get_by_id: {e}")
            return None
        except Exception as e:
            print(f"Exception in get_by_id: {e}")
            return None

    @staticmethod
    def update(recipe_id, data):
        """
        更新已存在的食譜記錄
        :param recipe_id: int
        :param data: dict，包含 title, ingredients, steps
        :return: bool (成功與否)
        """
        try:
            with get_db_connection() as conn:
                conn.execute(
                    "UPDATE recipes SET title = ?, ingredients = ?, steps = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (data.get('title'), data.get('ingredients'), data.get('steps'), recipe_id)
                )
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error in update: {e}")
            return False
        except Exception as e:
            print(f"Exception in update: {e}")
            return False

    @staticmethod
    def toggle_favorite(recipe_id):
        """
        切換食譜的收藏狀態
        :param recipe_id: int
        :return: int (新狀態0或1) 或 None
        """
        try:
            with get_db_connection() as conn:
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
        except sqlite3.Error as e:
            print(f"Database error in toggle_favorite: {e}")
            return None
        except Exception as e:
            print(f"Exception in toggle_favorite: {e}")
            return None

    @staticmethod
    def delete(recipe_id):
        """
        刪除一筆記錄
        :param recipe_id: int
        :return: bool (成功與否)
        """
        try:
            with get_db_connection() as conn:
                conn.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error in delete: {e}")
            return False
        except Exception as e:
            print(f"Exception in delete: {e}")
            return False
