step(
  """
  ALTER TABLE `badges` MODIFY `type` tinyint(1) unsigned NOT NULL;
  RENAME TABLE `events` TO `event`;
  ALTER TABLE `event_badges_events` DROP FOREIGN KEY `event_id`;
  ALTER TABLE `event_badges_events` ADD CONSTRAINT `fk_event_badges_events_1` FOREIGN KEY (`event_id`) REFERENCES `events` (`event_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
  ALTER TABLE `event_participant_badges` DROP FOREIGN KEY `event_id`;
  ALTER TABLE `event_participant_badges` CONSTRAINT `fk_event_participant_badges_1` FOREIGN KEY (`event_id`) REFERENCES `events` (`event_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
  ALTER TABLE `event_participants` DROP FOREIGN KEY `event_id`
  ALTER TABLE `event_participants` CONSTRAINT `fk_event_participants_1` FOREIGN KEY (`event_id`) REFERENCES `event` (`event_id`) ON DELETE CASCADE ON UPDATE NO ACTION
  """,
  """
  ALTER TABLE `badges` MODIFY `type` tinyint(4) unsigned NOT NULL;
  RENAME TABLE `event` TO `events`;
  ALTER TABLE `event_badges_events` DROP FOREIGN KEY `event_id`;
  ALTER TABLE `event_badges_events` ADD CONSTRAINT `fk_event_badges_events_1` FOREIGN KEY (`event_id`) REFERENCES `event` (`event_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
  ALTER TABLE `event_participant_badges` DROP FOREIGN KEY `event_id`;
  ALTER TABLE `event_participant_badges` CONSTRAINT `fk_event_participant_badges_1` FOREIGN KEY (`event_id`) REFERENCES `event` (`event_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
  ALTER TABLE `event_participants` DROP FOREIGN KEY `event_id`
  ALTER TABLE `event_participants` CONSTRAINT `fk_event_participants_1` FOREIGN KEY (`event_id`) REFERENCES `events` (`event_id`) ON DELETE CASCADE ON UPDATE NO ACTION;
  """,
  ignore_errors='apply'
)
