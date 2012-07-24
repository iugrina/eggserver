step(
  """
  CREATE TABLE `users` (
    `user_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
    `first_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
    `last_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
    `email` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
    PRIMARY KEY (`user_id`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

  CREATE TABLE `badges` (
      `badge_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
      `image_link` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
      `name` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
      `description` varchar(1000) COLLATE utf8_unicode_ci DEFAULT NULL,
      `parent` int(10) unsigned NOT NULL,
      `type` tinyint(4) unsigned NOT NULL,
      PRIMARY KEY (`badge_id`),
      KEY `parent` (`parent`),
      KEY `type` (`type`)
  ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

  CREATE TABLE `badges_users` (
      `badge_id` bigint(20) unsigned NOT NULL,
      `user_id` bigint(20) unsigned NOT NULL,
      `description` varchar(1000) COLLATE utf8_unicode_ci DEFAULT NULL,
      PRIMARY KEY (`badge_id`,`user_id`),
      KEY `badge_id` (`badge_id`),
      KEY `user_id` (`user_id`),
      CONSTRAINT `badges_users_ibfk_1` FOREIGN KEY (`badge_id`) REFERENCES `badges` (`badge_id`) ON DELETE CASCADE ON UPDATE CASCADE,
      CONSTRAINT `badges_users_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

  CREATE TABLE `events` (
      `event_id` bigint(20) unsigned NOT NULL,
      `name` varchar(255) DEFAULT NULL,
      `description` varchar(2000) DEFAULT NULL,
      `scheduled_for` datetime DEFAULT NULL,
      `expected_duration` time DEFAULT NULL,
      `registration_deadline` datetime DEFAULT NULL,
      `location` varchar(255) DEFAULT NULL,
      `hide_location` tinyint(1) DEFAULT NULL,
      `registration_price` decimal(10,2) DEFAULT NULL,
      `creation_price` decimal(10,2) DEFAULT NULL,
      `is_active` tinyint(1) DEFAULT NULL,
      `phase` enum('before_deadline','before_event','during_event','after_event') DEFAULT NULL,
      PRIMARY KEY (`event_id`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

  CREATE TABLE `event_badges` (
      `event_badge_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
      `link` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
      `name` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
      `description` varchar(1000) COLLATE utf8_unicode_ci DEFAULT NULL,
      `parent` bigint(20) unsigned DEFAULT NULL,
      `type` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
      PRIMARY KEY (`event_badge_id`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

  CREATE TABLE `event_badges_events` (
      `event_id` bigint(20) unsigned NOT NULL,
      `event_badge_id` bigint(20) unsigned NOT NULL,
      PRIMARY KEY (`event_id`,`event_badge_id`),
      KEY `fk_event_badges_events_1` (`event_id`),
      KEY `fk_event_badges_events_2` (`event_badge_id`),
      CONSTRAINT `fk_event_badges_events_1` FOREIGN KEY (`event_id`) REFERENCES `events` (`event_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
      CONSTRAINT `fk_event_badges_events_2` FOREIGN KEY (`event_badge_id`) REFERENCES `event_badges` (`event_badge_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

  CREATE TABLE `event_participant_badges` (
      `event_id` bigint(20) unsigned NOT NULL,
      `badge_id` bigint(20) unsigned NOT NULL,
      PRIMARY KEY (`event_id`,`badge_id`),
      KEY `fk_event_participant_badges_1` (`event_id`),
      KEY `fk_event_participant_badges_2` (`badge_id`),
      CONSTRAINT `fk_event_participant_badges_1` FOREIGN KEY (`event_id`) REFERENCES `events` (`event_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
      CONSTRAINT `fk_event_participant_badges_2` FOREIGN KEY (`badge_id`) REFERENCES `badges` (`badge_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

  CREATE TABLE `event_participants` (
      `event_id` bigint(20) unsigned NOT NULL,
      `user_id` bigint(20) unsigned NOT NULL,
      `participant_type` enum('organizer','guest','other') COLLATE utf8_unicode_ci DEFAULT NULL,
      `attending` enum('yes','no','maybe','unaccepted','undecided') COLLATE utf8_unicode_ci DEFAULT NULL,
      `other_participant_type` enum('random','guest_decision') COLLATE utf8_unicode_ci DEFAULT NULL,
      PRIMARY KEY (`event_id`,`user_id`),
      KEY `fk_event_participants_2` (`user_id`),
      CONSTRAINT `fk_event_participants_1` FOREIGN KEY (`event_id`) REFERENCES `events` (`event_id`) ON DELETE CASCADE ON UPDATE NO ACTION,
      CONSTRAINT `fk_event_participants_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

  CREATE TABLE `event_photos` (
      `event_id` bigint(20) unsigned NOT NULL,
      `photo_id` bigint(20) unsigned NOT NULL,
      `type` enum('before_event','after_event') COLLATE utf8_unicode_ci NOT NULL,
      PRIMARY KEY (`event_id`,`photo_id`),
      KEY `idx_event_photos_type` (`type`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
  """,
  """
  DROP TABLE users;
  DROP TABLE badges;
  DROP TABLE badges_users;
  DROP TABLE events;
  DROP TABLE event_badges;
  DROP TABLE event_badges_events;
  DROP TABLE event_participant_badges;
  DROP TABLE event_participants;
  DROP TABLE event_photos;
  """,
  ignore_errors='apply'
)
