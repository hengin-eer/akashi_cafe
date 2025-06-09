from flask import Flask, jsonify


def create_app():
    app = Flask(__name__)

    # Configuration
    app.config.from_pyfile("config.py")

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

    return app
