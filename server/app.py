from flask import Flask, jsonify
import dotenv
import psycopg2
from pathlib import Path


def create_app():
    app = Flask(__name__)

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

    @app.route("/account")
    def account():
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
