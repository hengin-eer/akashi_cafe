CREATE TABLE accounts (
  id varchar(6) NOT NULL PRIMARY KEY, -- 学籍番号
  name varchar(50) NOT NULL -- 氏名
);

-- 月替わりのメニュー
CREATE TABLE menu (
  id varchar(6) PRIMARY KEY, -- 固有ID
  date date NOT NULL, -- 日付
  type menu_type NOT NULL, -- メニューの種類
  name varchar(50) NOT NULL, -- メニュー名
  price int NOT NULL, -- 価格
  energy int NOT NULL, -- エネルギー量
  protein DECIMAL(3, 1) NOT NULL, -- タンパク質量
  fat DECIMAL(3, 1) NOT NULL, -- 脂質量
  carb DECIMAL(4, 1) NOT NULL, -- 炭水化物量
  salt DECIMAL(2, 1) NOT NULL, -- 食塩相当量
  allergens menu_allergens[] -- アレルゲン
);

-- 常設メニュー
CREATE TABLE permanent_menu (
  id varchar(6) PRIMARY KEY, -- 固有ID
  type permanent_menu_type NOT NULL, -- 常設メニューの種類
  name varchar(50) NOT NULL, -- メニュー名
  price int NOT NULL, -- 価格
  energy int NOT NULL, -- エネルギー量
  protein DECIMAL(3, 1) NOT NULL, -- タンパク質量
  fat DECIMAL(3, 1) NOT NULL, -- 脂質量
  carb DECIMAL(4, 1) NOT NULL, -- 炭水化物量
  salt DECIMAL(2, 1) NOT NULL, -- 食塩相当量
  allergens menu_allergens[] -- アレルゲン
);

-- NOTE: 常設メニューはテーブル上でいつ売られている、という情報を持たない
-- そのため、いつ売られているメニューを、いつ売り切れ報告がなされたか、で判断する必要がある
-- よって売り切れ情報を登録する際には当日のみの操作に限定する
CREATE TABLE permanent_menu_soldout (
  permanent_menu_id varchar(6) PRIMARY KEY, -- permanent_menuの外部キー
  soldout_at timestamp NOT NULL DEFAULT current_timestamp, -- 売り切れ日時
  reviewers varchar(6)[] NOT NULL, -- 売り切れを確認した学籍番号の配列
  unti_reviewers varchar(6)[] NOT NULL, -- 売り切れていないことを確認した学籍番号の配列
  CONSTRAINT fk_permanent_menu FOREIGN KEY (permanent_menu_id) REFERENCES permanent_menu(id)
);

CREATE TABLE daily_menu_soldout (
  daily_menu_id varchar(6) PRIMARY KEY, -- 日替わりメニューのID
  soldout_at timestamp NOT NULL DEFAULT current_timestamp, -- 売り切れ日時
  reviewers varchar(6)[] NOT NULL, -- 売り切れを確認した学籍番号の配列
  unti_reviewers varchar(6)[] NOT NULL, -- 売り切れていないことを確認した学籍番号の配列
  CONSTRAINT fk_daily_menu FOREIGN KEY (daily_menu_id) REFERENCES menu(id)
);
