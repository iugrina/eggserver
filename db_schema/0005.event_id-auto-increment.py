step(
  """
  ALTER TABLE  `events` CHANGE  `event_id`  `event_id` BIGINT( 20 ) UNSIGNED NOT NULL AUTO_INCREMENT
  """,
  """
  ALTER TABLE  `events` CHANGE  `event_id`  `event_id` BIGINT( 20 ) UNSIGNED NOT NULL
  """,
  ignore_errors='apply'
)