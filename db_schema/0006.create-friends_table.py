step(
  """
  CREATE TABLE `friends` (
    `user_id` bigint(20) unsigned NOT NULL,
    `friend_id` bigint(20) unsigned NOT NULL,
    `approved` tinyint(1) unsigned NOT NULL,
    PRIMARY KEY (`user_id`,`friend_id`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

  """,
  """
  DROP TABLE friends;
  """
)
