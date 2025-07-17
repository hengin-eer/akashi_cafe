CREATE TYPE menu_allergens AS ENUM ('小麦', '卵', '乳', 'そば', '落花生', 'えび', 'かに', 'くるみ');
CREATE TYPE menu_tags AS ENUM ('管理栄養士監修メニュー', '肉サラ', 'おすすめ', '人気メニュー', '魚を食べよう', 'Seasonal Menu');
CREATE TYPE menu_type AS ENUM ('A', 'B');
CREATE TYPE permanent_menu_type AS ENUM ('curry', 'bowl', 'ramen', 'jp-noodles', 'rice');
-- CREATE TYPE menu_classification AS ENUM ('daily', 'permanent');
