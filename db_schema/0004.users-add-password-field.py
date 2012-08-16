step(
  """
  ALTER TABLE `users` ADD COLUMN `password` varchar(1000) COLLATE utf8_unicode_ci DEFAULT NULL
  """,
  """
  ALTER TABLE `users` DROP COLUMN `password`
  """,
  ignore_errors='apply'
)
