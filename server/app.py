from flask import Flask, jsonify, request
import psycopg2
import csv
import io
from pathlib import Path
from flask_cors import CORS
from lib.parse_pg_enum_array import parse_pg_enum_array
from datetime import datetime


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

    @app.route("/admin/menu/upload", methods=["POST"])
    def upload_daily_menu_csv():
        """
        CSVファイルをアップロードして日替わりメニューをデータベースに追加するエンドポイント

        CSVフォーマット:
        id,date,type,name,price,energy,protein,fat,carb,salt,allergens

        例:
        D-0001,2025-07-01,A,白身魚のフリット レモンソース,430,578,18.8,13.3,97.5,2.6,"小麦,乳,そば,えび,かに,くるみ"
        """
        try:
            # CSVファイルの取得
            if "file" not in request.files:
                return jsonify({"error": "CSVファイルが見つかりません"}), 400

            file = request.files["file"]
            if file.filename == "":
                return jsonify({"error": "ファイルが選択されていません"}), 400

            if not file.filename.lower().endswith(".csv"):
                return jsonify({"error": "CSVファイルのみアップロード可能です"}), 400

            # CSVファイルの読み込み
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_reader = csv.DictReader(stream)

            # バリデーション用の必要カラム
            required_columns = [
                "id",
                "date",
                "type",
                "name",
                "price",
                "energy",
                "protein",
                "fat",
                "carb",
                "salt",
                "allergens",
            ]

            # CSVヘッダーのチェック
            if not all(col in csv_reader.fieldnames for col in required_columns):
                missing_cols = [
                    col for col in required_columns if col not in csv_reader.fieldnames
                ]
                return (
                    jsonify({"error": f"必要なカラムが不足しています: {missing_cols}"}),
                    400,
                )

            # データベース接続
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            inserted_count = 0
            errors = []

            try:
                for row_num, row in enumerate(
                    csv_reader, start=2
                ):  # ヘッダー行を除いて2行目から開始
                    try:
                        # データの前処理
                        menu_id = row["id"].strip()
                        date = row["date"].strip()
                        menu_type = row["type"].strip()
                        name = row["name"].strip()
                        price = int(row["price"].strip())
                        energy = int(row["energy"].strip())
                        protein = float(row["protein"].strip())
                        fat = float(row["fat"].strip())
                        carb = float(row["carb"].strip())
                        salt = float(row["salt"].strip())

                        # アレルゲンの処理（カンマ区切りの文字列をリストに変換）
                        allergens_str = row["allergens"].strip()
                        if allergens_str:
                            allergens_list = [
                                allergen.strip()
                                for allergen in allergens_str.split(",")
                            ]
                        else:
                            allergens_list = []

                        # 日付フォーマットのバリデーション
                        try:
                            datetime.strptime(date, "%Y-%m-%d")
                        except ValueError:
                            errors.append(
                                f"行 {row_num}: 日付フォーマットが正しくありません (YYYY-MM-DD形式で入力してください): {date}"
                            )
                            continue

                        # メニュータイプのバリデーション
                        if menu_type not in ["A", "B"]:
                            errors.append(
                                f"行 {row_num}: メニュータイプは 'A' または 'B' である必要があります: {menu_type}"
                            )
                            continue

                        # アレルゲンのバリデーション
                        valid_allergens = [
                            "小麦",
                            "卵",
                            "乳",
                            "そば",
                            "落花生",
                            "えび",
                            "かに",
                            "くるみ",
                        ]
                        invalid_allergens = [
                            a for a in allergens_list if a not in valid_allergens
                        ]
                        if invalid_allergens:
                            errors.append(
                                f"行 {row_num}: 無効なアレルゲンが含まれています: {invalid_allergens}"
                            )
                            continue

                        # データベースへの挿入
                        insert_sql = """
                        INSERT INTO menu (id, date, type, name, price, energy, protein, fat, carb, salt, allergens)
                        VALUES (%s, %s, %s::menu_type, %s, %s, %s, %s, %s, %s, %s, %s::menu_allergens[])
                        """
                        cursor.execute(
                            insert_sql,
                            [
                                menu_id,
                                date,
                                menu_type,
                                name,
                                price,
                                energy,
                                protein,
                                fat,
                                carb,
                                salt,
                                allergens_list,
                            ],
                        )
                        inserted_count += 1

                    except psycopg2.IntegrityError as e:
                        if "duplicate key" in str(e):
                            errors.append(
                                f"行 {row_num}: メニューID '{menu_id}' は既に存在します"
                            )
                        else:
                            errors.append(
                                f"行 {row_num}: データベースエラー - {str(e)}"
                            )
                        conn.rollback()
                        continue
                    except (ValueError, TypeError) as e:
                        errors.append(f"行 {row_num}: データ型エラー - {str(e)}")
                        continue
                    except Exception as e:
                        errors.append(f"行 {row_num}: 予期しないエラー - {str(e)}")
                        continue

                # トランザクションのコミット
                if inserted_count > 0 and not errors:
                    conn.commit()
                    return (
                        jsonify(
                            {
                                "message": f"日替わりメニューを {inserted_count} 件追加しました",
                                "inserted_count": inserted_count,
                            }
                        ),
                        200,
                    )
                elif inserted_count > 0 and errors:
                    conn.commit()
                    return (
                        jsonify(
                            {
                                "message": f"日替わりメニューを {inserted_count} 件追加しました（一部エラーあり）",
                                "inserted_count": inserted_count,
                                "errors": errors,
                            }
                        ),
                        207,
                    )  # 207 Multi-Status
                else:
                    conn.rollback()
                    return (
                        jsonify(
                            {"error": "メニューの追加に失敗しました", "errors": errors}
                        ),
                        400,
                    )

            except Exception as e:
                conn.rollback()
                return (
                    jsonify(
                        {"error": f"データベース処理中にエラーが発生しました: {str(e)}"}
                    ),
                    500,
                )
            finally:
                cursor.close()
                conn.close()

        except Exception as e:
            return (
                jsonify(
                    {"error": f"CSVファイルの処理中にエラーが発生しました: {str(e)}"}
                ),
                500,
            )

    return app
