create table accounts (
  id varchar(6) not null primary key, -- 学籍番号
  name varchar(50) not null -- 氏名
);

-- 月替わりのメニュー
create table menu (
  date date not null, -- 日付
  type menu_type not null, -- メニューの種類
  name varchar(50) not null, -- メニュー名
  price int not null, -- 価格
  energy int not null, -- エネルギー量
  protein DECIMAL(3, 1) not null, -- タンパク質量
  fat DECIMAL(3, 1) not null, -- 脂質量
  carb DECIMAL(4, 1) not null, -- 炭水化物量
  salt DECIMAL(2, 1) not null, -- 食塩相当量
  allergens menu_allergens[], -- アレルゲン
  tags menu_tags -- メニューのタグ
);

-- 常設メニュー
create table permanent_menu (
  id varchar(6) primary key, -- 固有ID
  type permanent_menu_type not null, -- 常設メニューの種類
  name varchar(50) not null, -- メニュー名
  price int not null, -- 価格
  energy int not null, -- エネルギー量
  protein DECIMAL(3, 1) not null, -- タンパク質量
  fat DECIMAL(3, 1) not null, -- 脂質量
  carb DECIMAL(4, 1) not null, -- 炭水化物量
  salt DECIMAL(2, 1) not null, -- 食塩相当量
  allergens menu_allergens[] -- アレルゲン
);

-- create table soldouts (
--   id uuid primary key, -- UUID
--   menu_class menu_classification not null, -- メニュー：日替わり or 常設
--   menu_date date, -- 日替わりの場合のみ使用
--   daily_menu_name varchar(50), -- 日替わりの場合のメニュー名（permanentならNULL）
--   permanent_menu_id int, -- permanent_menuの外部キー（dailyならNULL）

--   created_at timestamp not null default current_timestamp,
--   soldout_reviewers varchar(6)[] not null, -- 学籍番号の配列
--   unsoldout_reviewers varchar(6)[] not null, -- 学籍番号の配列

--   constraint fk_permanent_menu foreign key (permanent_menu_id) references permanent_menu(id),
--   constraint check_menu_ref check (
--     (menu_type = 'daily' and menu_date is not null and daily_menu_name is not null and permanent_menu_id is null) or
--     (menu_type = 'permanent' and permanent_menu_id is not null and menu_date is null and daily_menu_name is null)
--   )
-- );
