create table accounts (
  id varchar(6) not null primary key, -- 学籍番号
  name varchar(50) not null -- 氏名
);

-- 月替わりのメニュー
create table menu (
  id varchar(6) primary key, -- 固有ID
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

-- NOTE: 常設メニューはテーブル上でいつ売られている、という情報を持たない
-- そのため、いつ売られているメニューを、いつ売り切れ報告がなされたか、で判断する必要がある
-- よって売り切れ情報を登録する際には当日のみの操作に限定する
create table permanent_menu_soldout (
  permanent_menu_id varchar(6) primary key, -- permanent_menuの外部キー
  soldout_at timestamp not null default current_timestamp, -- 売り切れ日時
  reviewers varchar(6)[] not null, -- 売り切れを確認した学籍番号の配列
  unti_reviewers varchar(6)[] not null, -- 売り切れていないことを確認した学籍番号の配列
  constraint fk_permanent_menu foreign key (permanent_menu_id) references permanent_menu(id)
);

create table daily_menu_soldout (
  daily_menu_id varchar(6) primary key, -- 日替わりメニューのID
  soldout_at timestamp not null default current_timestamp, -- 売り切れ日時
  reviewers varchar(6)[] not null, -- 売り切れを確認した学籍番号の配列
  unti_reviewers varchar(6)[] not null, -- 売り切れていないことを確認した学籍番号の配列
  constraint fk_daily_menu foreign key (daily_menu_id) references menu(id)
);
