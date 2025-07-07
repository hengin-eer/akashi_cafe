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
        日付を指定してその日のメニューを取得するエンドポイント
        """
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        try:
            sql = read_sql("sql/get_menu_by_day.sql")
            cursor.execute(sql, [date])
            menu_items = cursor.fetchall()
            menu_list = [
                {
                    "id": item[0],
                    "date": item[1].isoformat(),
                    "type": item[2],
                    "name": item[3],
                    "price": item[4],
                    "energy": item[5],
                    "protein": float(item[6]),
                    "fat": float(item[7]),
                    "carb": float(item[8]),
                    "salt": float(item[9]),
                    "allergens": parse_pg_enum_array(item[10]),
                }
                for item in menu_items
            ]
            return jsonify(menu_list)
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
