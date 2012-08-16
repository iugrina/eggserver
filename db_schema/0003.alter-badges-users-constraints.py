step(
  """
  ALTER TABLE `badges_users` DROP FOREIGN KEY `badges_users_ibfk_1`;
  ALTER TABLE `badges_users` DROP FOREIGN KEY `badges_users_ibfk_2`;
  ALTER TABLE `badges_users` ADD CONSTRAINT `badges_users_ibfk_1` FOREIGN KEY (`badge_id`) REFERENCES `badges` (`badge_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
  ALTER TABLE `badges_users` ADD CONSTRAINT `badges_users_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
  """,
  """
  ALTER TABLE `badges_users` DROP FOREIGN KEY `badges_users_ibfk_1`;
  ALTER TABLE `badges_users` DROP FOREIGN KEY `badges_users_ibfk_2`;
  ALTER TABLE `badges_users` ADD CONSTRAINT `badges_users_ibfk_1` FOREIGN KEY (`badge_id`) REFERENCES `badges` (`badge_id`) ON DELETE CASCADE ON UPDATE CASCADE;
  ALTER TABLE `badges_users` ADD CONSTRAINT `badges_users_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;
  """
)
