SELECT
  pm.id,
  pm.type,
  pm.name,
  pm.price,
  pm.energy,
  pm.protein,
  pm.fat,
  pm.carb,
  pm.salt,
  pm.allergens,
  pms.reviewers,
  pms.unti_reviewers
FROM
  permanent_menu AS pm
LEFT JOIN
  permanent_menu_soldout AS pms ON pm.id = pms.permanent_menu_id
ORDER BY
  pm.id;
