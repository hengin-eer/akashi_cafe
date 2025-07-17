SELECT
  m.id,
  m.type,
  m.name,
  m.price,
  m.energy,
  m.protein,
  m.fat,
  m.carb,
  m.salt,
  m.allergens,
  dms.reviewers,
  dms.unti_reviewers
FROM
  menu AS m
LEFT JOIN
  daily_menu_soldout AS dms ON m.id = dms.daily_menu_id
WHERE
  m.date = %s
ORDER BY
  m.id;
-- $1: menu.date
