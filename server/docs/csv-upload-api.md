# CSVアップロードAPI仕様書

## 概要
日替わりメニューのCSVファイルをアップロードして、データベースのmenuテーブルに一括で追加するAPIです。

## エンドポイント
```
POST /admin/menu/upload
```

## リクエスト形式
- Content-Type: multipart/form-data
- パラメータ: `file` (CSVファイル)

## CSVファイルの形式

### 必須カラム
| カラム名 | データ型 | 説明 | 例 |
|---------|---------|------|-----|
| id | string | メニューの固有ID | D-9001 |
| date | string | 提供日付（YYYY-MM-DD形式） | 2025-08-01 |
| type | string | メニュータイプ（A または B） | A |
| name | string | メニュー名 | 鶏の照り焼き |
| price | integer | 価格（円） | 430 |
| energy | integer | エネルギー量（kcal） | 650 |
| protein | float | タンパク質量（g） | 25.5 |
| fat | float | 脂質量（g） | 18.2 |
| carb | float | 炭水化物量（g） | 95.8 |
| salt | float | 食塩相当量（g） | 3.2 |
| allergens | string | アレルゲン（カンマ区切り） | "小麦,そば" |

### CSVサンプル
```csv
id,date,type,name,price,energy,protein,fat,carb,salt,allergens
D-9001,2025-08-01,A,鶏の照り焼き,430,650,25.5,18.2,95.8,3.2,"小麦,そば"
D-9002,2025-08-01,B,豚丼,380,720,22.0,20.5,105.0,4.1,"小麦,そば,えび"
```

## アレルゲンの有効値
- 小麦
- 卵
- 乳
- そば
- 落花生
- えび
- かに
- くるみ

## レスポンス

### 成功時（200 OK）
すべてのレコードが正常に挿入された場合
```json
{
  "message": "日替わりメニューを 4 件追加しました",
  "inserted_count": 4
}
```

### 部分成功時（207 Multi-Status）
一部のレコードでエラーが発生した場合
```json
{
  "message": "日替わりメニューを 2 件追加しました（一部エラーあり）",
  "inserted_count": 2,
  "errors": [
    "行 3: メニューID 'D-9003' は既に存在します",
    "行 4: 日付フォーマットが正しくありません (YYYY-MM-DD形式で入力してください): 2025/08/02"
  ]
}
```

### エラー時（400 Bad Request）
```json
{
  "error": "CSVファイルが見つかりません"
}
```

```json
{
  "error": "必要なカラムが不足しています: ['price', 'energy']"
}
```

```json
{
  "error": "メニューの追加に失敗しました",
  "errors": [
    "行 2: データ型エラー - invalid literal for int() with base 10: 'abc'",
    "行 3: 無効なアレルゲンが含まれています: ['大豆']"
  ]
}
```

### サーバーエラー時（500 Internal Server Error）
```json
{
  "error": "データベース処理中にエラーが発生しました: connection timeout"
}
```

## バリデーション

### データ型チェック
- price, energy: 整数
- protein, fat, carb, salt: 浮動小数点数
- date: YYYY-MM-DD形式の日付文字列

### 制約チェック
- id: 重複不可（既存のメニューIDと重複した場合はスキップ）
- type: 'A' または 'B' のみ
- allergens: 有効なアレルゲンのみ

## 使用例

### cURLでのテスト
```bash
curl -X POST \
  -F "file=@sample_daily_menu.csv" \
  http://localhost:8084/admin/menu/upload
```

### Pythonでのテスト
```python
import requests

url = "http://localhost:8084/admin/menu/upload"
files = {"file": open("sample_daily_menu.csv", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

## 注意事項

1. **文字エンコーディング**: CSVファイルはUTF-8エンコーディングで保存してください
2. **トランザクション**: エラーが発生した行は挿入されませんが、正常な行は挿入されます
3. **重複ID**: 既に存在するメニューIDがある場合、その行はスキップされエラーとして報告されます
4. **ファイルサイズ**: 大きなファイルの場合は、分割してアップロードすることを推奨します
5. **セキュリティ**: 本APIは管理者用のため、適切な認証・認可機能を追加することを推奨します
