insert into menu (id, date, type, name, price, energy, protein, fat, carb, salt, allergens) values
('D-0001', '2025-07-01', 'A'::menu_type, '白身魚のフリット レモンソース', 430, 578, 18.8, 13.3, 97.5, 2.6, ARRAY['小麦', '卵', '乳']::menu_allergens[]),
('D-0002', '2023-07-01', 'B'::menu_type, '豚塩カルビ丼', 380, 605, 20.3, 17.3, 96.0, 2.7, ARRAY[]::menu_allergens[]);
