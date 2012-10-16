step(
  """
  CREATE TABLE `blacklist` (
    `user_id` bigint(20) unsigned NOT NULL,
    `blacklisted_id` bigint(20) unsigned NOT NULL,
    PRIMARY KEY (`user_id`, `blacklisted_id`),
    CONSTRAINT `blacklist_fk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `blacklist_fk_2` FOREIGN KEY (`blacklisted_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
  """,
  """
  DROP TABLE `blacklist`;
  """,
  ignore_errors='apply'
)
