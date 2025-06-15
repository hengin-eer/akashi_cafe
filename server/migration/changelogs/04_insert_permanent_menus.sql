insert into permanent_menu (id, type, name, price, energy, protein, fat, carb, salt, allergens) values
('M-0001', 'curry', 'カレーライス(中辛)', 300, 561, 8.9, 10.5, 110.8, 4.0, ARRAY['小麦']::menu_allergens[]),
('M-0002', 'curry', 'ポークカツカレー', 380, 771, 14.5, 22.3, 131.0, 4.8, ARRAY['小麦', '卵', '乳']::menu_allergens[]),
('M-0003', 'bowl', '親子丼', 350, 701, 29.3, 18.4, 105.0, 3.3, ARRAY['小麦', '卵']::menu_allergens[]),
('M-0004', 'bowl', 'かつ丼', 350, 735, 20.6, 18.4, 123.6, 3.7, ARRAY['小麦', '卵', '乳']::menu_allergens[]),
('M-0005', 'ramen', '醤油ラーメン', 250, 437, 17.2, 6.4, 73.5, 7.5, ARRAY['小麦', '卵']::menu_allergens[]),
('M-0006', 'ramen', 'とんこつラーメン', 250, 476, 20.2, 8.0, 76.5, 8.0, ARRAY['小麦', '卵']::menu_allergens[]),
('M-0007', 'ramen', '味噌ラーメン', 250, 530, 20.0, 11.9, 81.4, 9.4, ARRAY['小麦', '卵']::menu_allergens[]),
('M-0008', 'jp-noodles', 'かけうどん・そば', 200, 355, 13.2, 2.2, 67.3, 4.2, ARRAY['小麦', '卵', '乳', 'そば', 'えび']::menu_allergens[]),
('M-0009', 'rice', 'ライス中(210g)', 120, 328, 5.3, 0.6, 77.9, 0.0, null);
