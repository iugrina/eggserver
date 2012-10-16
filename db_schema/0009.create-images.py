step(
  """
  CREATE TABLE `profile_images` (
    `image_id` bigint(20) unsigned NOT NULL,
    `user_id` bigint(20) unsigned NOT NULL,
    `order_id` int unsigned NOT NULL,
    `created` datetime NOT NULL,
    `description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
    `type` enum('profile','friend','other') NOT NULL,
    `visibility` tinyint(4) unsigned NOT NULL,
    `extension` varchar(5) DEFAULT NULL,
    PRIMARY KEY (`image_id`, `user_id`),
    CONSTRAINT `images_fk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
  """,
  """
  DROP TABLE `profile_images`;
  """,
  ignore_errors='apply'
)
