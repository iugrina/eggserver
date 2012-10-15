step(
  """
  DROP TABLE IF EXISTS friends;

  CREATE TABLE `friends` (
    `user_id` bigint(20) unsigned NOT NULL,
    `friend_id` bigint(20) unsigned NOT NULL,
    `approved` tinyint(1) unsigned NOT NULL,
    PRIMARY KEY (`user_id`,`friend_id`),
    CONSTRAINT `friends_fk1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `friends_fk2` FOREIGN KEY (`friend_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

  """,
  """
  DROP TABLE friends;
  """
)
