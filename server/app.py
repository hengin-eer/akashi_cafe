from flask import Flask, jsonify
import psycopg2
from pathlib import Path
from flask_cors import CORS
from lib.parse_pg_enum_array import parse_pg_enum_array


def create_app():
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:3000", "http://localhost:4173"])

    db_config = {
        "host": "localhost",
        "database": "akashi_cafe",
        "port": 5432,
        "user": "root",
        "password": "team4",
    }

    def read_sql(file_path):
        return Path(file_path).read_text(encoding="utf-8")

    @app.route("/")
    def index():
        return "Welcome to Akashi Cafe!"

    @app.route("/menu")
    def menu():
        # メニューデータを返す
        # ここではダミーデータを使用していますが、実際にはデータベースから取得することを想定しています。
        dummy_menu = [
            {"id": 1, "name": "コーヒー", "price": 400},
            {"id": 2, "name": "紅茶", "price": 350},
            {"id": 3, "name": "サンドイッチ", "price": 600},
        ]
        return jsonify(dummy_menu)

    @app.route("/menu/<date>")
    def menu_by_day(date):
        """
        日付を指定してその日のメニュー全てを取得するエンドポイント
        営業状態も含めて返す
        """
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        try:
            doday_sql = read_sql("sql/get_menus_by_date.sql")
            permanent_sql = read_sql("sql/get_all_permanent_menus.sql")
            # 日替わりメニューの取得
            cursor.execute(doday_sql, [date])
            today_menu_items = cursor.fetchall()

            # 営業状態を判定（日替わりメニューが存在するかどうか）
            is_open = len(today_menu_items) > 0

            if not is_open:
                # 営業していない場合
                return jsonify(
                    {
                        "status": "closed",
                        "message": "本日は営業しておりません",
                        "menus": [],
                    }
                )

            # 常設メニューの取得
            """
            TODO: 常設メニューの内、1つのラーメンを残して残りを除去する
            あとで設定画面を作る必要がある～
            が、あとまわしや（デモ時までに対応する必要はない）
            """
            cursor.execute(permanent_sql)
            permanent_menu_items = cursor.fetchall()
            menu_items = today_menu_items + permanent_menu_items
            menu_list = [
                {
                    "id": item[0],
                    "type": item[1],
                    "name": item[2],
                    "price": item[3],
                    "energy": item[4],
                    "protein": float(item[5]),
                    "fat": float(item[6]),
                    "carb": float(item[7]),
                    "salt": float(item[8]),
                    "allergens": parse_pg_enum_array(item[9]),
                }
                for item in menu_items
            ]

            # 営業中の場合
            return jsonify(
                {"status": "open", "message": "営業中です", "menus": menu_list}
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()

    @app.route("/menu/permanent/<menu_id>")
    def permanent_menu_by_id(menu_id):
        """
        常設メニューのレコードをIDで取得するエンドポイント
        """
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        try:
            sql = read_sql("sql/get_permanent_menu_by_id.sql")
            cursor.execute(sql, [menu_id])
            menu_item = cursor.fetchone()
            if menu_item:
                menu_data = {
                    "id": menu_item[0],
                    "type": menu_item[1],
                    "name": menu_item[2],
                    "price": menu_item[3],
                    "energy": menu_item[4],
                    "protein": float(menu_item[5]),
                    "fat": float(menu_item[6]),
                    "carb": float(menu_item[7]),
                    "salt": float(menu_item[8]),
                    "allergens": parse_pg_enum_array(menu_item[9]),
                }
                return jsonify(menu_data)
            else:
                return jsonify({"error": "Menu item not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()

    @app.route("/menu/permanent/all")
    def permanent_menu_all():
        """
        常設メニューのレコード全件を取得するエンドポイント
        """
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        try:
            sql = read_sql("sql/get_all_permanent_menus.sql")
            cursor.execute(sql)
            menu_items = cursor.fetchall()
            menu_list = [
                {
                    "id": item[0],
                    "type": item[1],
                    "name": item[2],
                    "price": item[3],
                    "energy": item[4],
                    "protein": float(item[5]),
                    "fat": float(item[6]),
                    "carb": float(item[7]),
                    "salt": float(item[8]),
                    "allergens": parse_pg_enum_array(item[9]),
                }
                for item in menu_items
            ]
            return jsonify(menu_list)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()

    @app.route("/accounts")
    def accounts():
        """
        全アカウント情報を取得するエンドポイント
        """
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        try:
            sql = read_sql("sql/get_accounts.sql")
            cursor.execute(sql)
            accounts = cursor.fetchall()
            account_list = [{"id": acc[0], "name": acc[1]} for acc in accounts]
            return jsonify(account_list)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()

    return app
