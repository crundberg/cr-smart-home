# Changelog

## 2015-12-27
- Added authentication to API, run `sudo pip install flask-httpauth` before first startup.

## 2015-12-28
Updated database, run the following SQL-query.
```
USE homeautomation;
ALTER TABLE `ha_lamp_objects` DROP `LampIO`;
ALTER TABLE `ha_lamp_objects` ADD `LampOrder` INT(11) NOT NULL DEFAULT '100' ;

DROP PROCEDURE `GetLampSchedulesSimple`; CREATE DEFINER=`root`@`localhost` PROCEDURE `GetLampSchedulesSimple`() COMMENT 'Get lamp schedules for today and yesterday' NOT DETERMINISTIC READS SQL DATA SQL SECURITY DEFINER SELECT t3.LampId, t3.LampName, t3.LampPowerOn, t3.LampCmdOn, t3.LampCmdOff, t1.ScheduleWeekday, t1.ScheduleTimeOn, t1.ScheduleTimeOff, t1.ScheduleMode FROM ha_lamp_objects t3 LEFT JOIN ha_lamp_schedule t1 on t1.ScheduleLampId = t3.LampId WHERE t1.ScheduleWeekday = WEEKDAY(NOW()) OR t1.ScheduleWeekday = WEEKDAY(DATE_SUB(NOW(), INTERVAL 1 DAY)) ORDER BY t3.LampId
```

## 2015-12-29
Updated database for logging and settings
```
USE homeautomation;

CREATE TABLE IF NOT EXISTS `ha_log` (
`LogId` int(11) NOT NULL,
  `LogDate` datetime NOT NULL,
  `LogName` varchar(250) NOT NULL,
  `LogLevel` varchar(50) NOT NULL,
  `LogMessage` text NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `ha_settings` (
`SettingId` int(11) NOT NULL,
  `SettingName` varchar(250) NOT NULL,
  `SettingValue` varchar(250) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

INSERT INTO `ha_settings` (`SettingId`, `SettingName`, `SettingValue`) VALUES
(1, 'Version', 'v0.1');

ALTER TABLE `ha_log`
 ADD PRIMARY KEY (`LogId`);
 
ALTER TABLE `ha_settings`
 ADD PRIMARY KEY (`SettingId`);
 
ALTER TABLE `ha_settings` CHANGE `SettingId` `SettingId` INT( 11 ) NOT NULL AUTO_INCREMENT ;
```

## 2015-12-30
Moved some settings from config-file to database.

## 2016-01-02
Added room feature.