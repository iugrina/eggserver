step(
  """
  ALTER TABLE  `users` CHANGE  `user_id`  `user_id` BIGINT( 20 ) UNSIGNED NOT NULL AUTO_INCREMENT ,
  CHANGE  `first_name`  `first_name` VARCHAR( 60 ) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL ,
  CHANGE  `last_name`  `last_name` VARCHAR( 60 ) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL ,
  CHANGE  `email`  `username` VARCHAR( 120 ) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL ,
  CHANGE  `password`  `password` VARCHAR( 100 ) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL;
  ALTER TABLE  `users` ADD  `nickname` VARCHAR( 100 ) NULL AFTER  `last_name`;
  ALTER TABLE  `users` ADD  `dob` DATETIME NULL DEFAULT NULL AFTER  `password` ,
  ADD  `created` DATETIME NOT NULL AFTER  `dob` ,
  ADD  `active` TINYINT NOT NULL AFTER  `created`
  """,
  """
  ALTER TABLE  `users` CHANGE  `user_id`  `user_id` BIGINT( 20 ) UNSIGNED NOT NULL AUTO_INCREMENT ,
  CHANGE  `first_name`  `first_name` VARCHAR( 255 ) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL ,
  CHANGE  `last_name`  `last_name` VARCHAR( 255 ) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL ,
  CHANGE  `username`  `email` VARCHAR( 255 ) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL ,
  CHANGE  `password`  `password` VARCHAR( 1000 ) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL;
  ALTER TABLE `users`  DROP `nickname`;
  ALTER TABLE `users`  DROP `dob`,  DROP `created`,  DROP `active`;
  """,
  ignore_errors='apply'
)