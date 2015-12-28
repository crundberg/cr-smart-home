# Changelog

## 2015-12-27
- Added authentication to API, run `sudo pip install flask-httpauth` before first startup.

## 2015-12-28
Updated database, run the following SQL-query.
```
USE homeautomation;
ALTER TABLE `ha_lamp_objects` DROP `LampIO`;
ALTER TABLE `ha_lamp_objects` ADD `LampOrder` INT(11) NOT NULL DEFAULT '100' ;

DROP PROCEDURE `GetLampSchedulesSimple`; CREATE DEFINER=`root`@`%` PROCEDURE `GetLampSchedulesSimple`() COMMENT 'Get lamp schedules for today and yesterday' NOT DETERMINISTIC READS SQL DATA SQL SECURITY DEFINER SELECT t3.LampId, t3.LampName, t3.LampPowerOn, t3.LampCmdOn, t3.LampCmdOff, t1.ScheduleWeekday, t1.ScheduleTimeOn, t1.ScheduleTimeOff, t1.ScheduleMode FROM ha_lamp_objects t3 LEFT JOIN ha_lamp_schedule t1 on t1.ScheduleLampId = t3.LampId WHERE t1.ScheduleWeekday = WEEKDAY(NOW()) OR t1.ScheduleWeekday = WEEKDAY(DATE_SUB(NOW(), INTERVAL 1 DAY)) ORDER BY t3.LampId
```