select id, type, name, price, energy, protein, fat, carb, salt, allergens from menu
where date = %s
order by id;
-- $1: menu.date
