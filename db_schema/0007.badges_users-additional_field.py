step(
  """
  ALTER TABLE  `badges_users` ADD `visibility` TINYINT(3);
  """,
  """
  ALTER TABLE  `badges_users` DELETE `visibility`;
  """,
  ignore_errors='apply'
)
