step(
  """
  ALTER TABLE  `users` CHANGE  `dob`  `dob` DATE NULL DEFAULT NULL;
  """,
  """
  ALTER TABLE  `users` CHANGE  `dob`  `dob` DATETIME NULL DEFAULT NULL;
  """,
  ignore_errors='apply'
)
