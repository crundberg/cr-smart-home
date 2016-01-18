-- phpMyAdmin SQL Dump
-- version 4.2.12deb2+deb8u1
-- http://www.phpmyadmin.net
--
-- Värd: localhost
-- Tid vid skapande: 18 jan 2016 kl 19:29
-- Serverversion: 5.5.44-0+deb8u1
-- PHP-version: 5.6.14-0+deb8u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Databas: `crsmarthome`
--
CREATE DATABASE IF NOT EXISTS `crsmarthome` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `crsmarthome`;

--
-- User: `hauser `
--
GRANT USAGE ON *.* TO 'hauser'@'localhost' IDENTIFIED BY PASSWORD '*07BE3499235CA0B7EE65F34EB34DACFE9CFD9942';
GRANT ALL PRIVILEGES ON `crsmarthome`.* TO 'hauser'@'localhost' WITH GRANT OPTION;

DELIMITER $$
--
-- Procedurer
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetLampSchedule`()
    READS SQL DATA
SELECT t3.LampId, t3.LampName, t3.LampPowerOn, t3.LampCmdOn, t3.LampCmdOff, t1.ScheduleWeekday, t1.ScheduleMode,
UNIX_TIMESTAMP(IF(t1.ScheduleWeekday = WEEKDAY(CURDATE()), CONCAT_WS(' ',CURDATE(), t1.ScheduleTimeOn), CONCAT_WS(' ',DATE_SUB(CURDATE(), INTERVAL 1 DAY), t1.ScheduleTimeOn))) as ScheduleTimeOn, 

UNIX_TIMESTAMP(IF (t1.ScheduleTimeOn > t1.ScheduleTimeOff,
	IF(t1.ScheduleWeekday = WEEKDAY(CURDATE()), CONCAT_WS(' ',DATE_ADD(CURDATE(), INTERVAL 1 DAY), t1.ScheduleTimeOff), CONCAT_WS(' ',CURDATE(), t1.ScheduleTimeOff)),
	IF(t1.ScheduleWeekday = WEEKDAY(CURDATE()), CONCAT_WS(' ',CURDATE(), t1.ScheduleTimeOff), CONCAT_WS(' ',DATE_SUB(CURDATE(), INTERVAL 1 DAY), t1.ScheduleTimeOff))
)) as ScheduleTimeOff

FROM ha_lamp_objects t3
LEFT JOIN ha_lamp_schedule t1 on t1.ScheduleLampId = t3.LampId
WHERE t1.ScheduleWeekday = WEEKDAY(NOW()) OR t1.ScheduleWeekday = WEEKDAY(DATE_SUB(NOW(), INTERVAL 1 DAY)) ORDER BY t3.LampId$$

CREATE DEFINER=`root`@`%` PROCEDURE `GetLampSchedulesSimple`()
    READS SQL DATA
    COMMENT 'Get lamp schedules for today and yesterday'
SELECT t3.LampId, t3.LampName, t3.LampPowerOn, t3.LampCmdOn, t3.LampCmdOff, t1.ScheduleWeekday, t1.ScheduleTimeOn, t1.ScheduleTimeOff, t1.ScheduleMode
FROM ha_lamp_objects t3
LEFT JOIN ha_lamp_schedule t1 on t1.ScheduleLampId = t3.LampId
WHERE t1.ScheduleWeekday = WEEKDAY(NOW()) OR t1.ScheduleWeekday = WEEKDAY(DATE_SUB(NOW(), INTERVAL 1 DAY))
ORDER BY t3.LampId$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Tabellstruktur `ha_data`
--

CREATE TABLE IF NOT EXISTS `ha_data` (
`DataId` int(11) NOT NULL,
  `DataName` varchar(250) NOT NULL,
  `DataText` text NOT NULL,
  `DataStatus` int(11) NOT NULL,
  `DataLastUpdated` datetime NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=latin1;

--
-- Dumpning av Data i tabell `ha_data`
--

INSERT INTO `ha_data` (`DataId`, `DataName`, `DataText`, `DataStatus`, `DataLastUpdated`) VALUES
(1, 'Schedule', 'OK', 200, '2016-01-18 19:29:00'),
(2, 'Weather', '{"message":"accurate","cod":"200","count":1,"list":[{"id":2689287,"name":"Gothenburg","coord":{"lon":11.9682,"lat":57.7007},"main":{"temp":-2,"pressure":1012,"humidity":92,"temp_min":-2,"temp_max":-2},"dt":1453135800,"wind":{"speed":3.1,"deg":200},"sys":{"country":"Sweden"},"clouds":{"all":75},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}]}]}\n', 200, '2016-01-18 18:30:24'),
(3, 'Sun', '{"Sunrise":"2016-01-18 08:40:00","Sunset":"2016-01-18 16:05:00"}', 200, '2016-01-18 19:00:02'),
(9999, 'Test', 'Test', 200, '2016-01-18 18:30:24');

-- --------------------------------------------------------

--
-- Tabellstruktur `ha_lamp_objects`
--

CREATE TABLE IF NOT EXISTS `ha_lamp_objects` (
`LampId` int(11) NOT NULL,
  `LampRoomId` int(11) DEFAULT NULL,
  `LampName` varchar(255) NOT NULL,
  `LampType` varchar(255) NOT NULL,
  `LampPowerOn` tinyint(2) NOT NULL,
  `LampPowerOnMan` tinyint(2) NOT NULL,
  `LampCmdOn` varchar(255) NOT NULL,
  `LampCmdOff` varchar(255) NOT NULL,
  `LampIncInAll` tinyint(2) NOT NULL DEFAULT '1',
  `LampOrder` int(11) NOT NULL DEFAULT '100'
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

--
-- Dumpning av Data i tabell `ha_lamp_objects`
--

INSERT INTO `ha_lamp_objects` (`LampId`, `LampRoomId`, `LampName`, `LampType`, `LampPowerOn`, `LampPowerOnMan`, `LampCmdOn`, `LampCmdOff`, `LampIncInAll`, `LampOrder`) VALUES
(1, NULL, 'Hall', 'Nexa', 0, 1, '262165', '262164', 1, 1),
(2, 1, 'FÃ¶nster', 'Nexa', 1, 1, '278549', '278548', 1, 2),
(3, 1, 'TV', 'Nexa', 0, 1, '266261', '266260', 1, 3),
(9, NULL, 'Bar', 'Nexa', 0, 0, '283925', '283924', 0, 4),
(10, NULL, 'Test', 'Nexa', 0, 0, '1234', '1234', 0, 5);

-- --------------------------------------------------------

--
-- Tabellstruktur `ha_lamp_schedule`
--

CREATE TABLE IF NOT EXISTS `ha_lamp_schedule` (
`ScheduleId` int(11) NOT NULL,
  `ScheduleLampId` int(11) NOT NULL,
  `ScheduleWeekday` int(11) NOT NULL,
  `ScheduleTimeOn` time NOT NULL,
  `ScheduleTimeOff` time NOT NULL,
  `ScheduleMode` int(11) NOT NULL DEFAULT '0' COMMENT '0=Inactive, 1=On, 2=On if sun is down'
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=latin1;

--
-- Dumpning av Data i tabell `ha_lamp_schedule`
--

INSERT INTO `ha_lamp_schedule` (`ScheduleId`, `ScheduleLampId`, `ScheduleWeekday`, `ScheduleTimeOn`, `ScheduleTimeOff`, `ScheduleMode`) VALUES
(1, 1, 0, '14:30:00', '22:00:00', 0),
(2, 1, 1, '14:30:00', '22:00:00', 0),
(3, 1, 2, '14:30:00', '22:00:00', 0),
(4, 1, 3, '14:30:00', '22:00:00', 0),
(5, 1, 4, '13:00:00', '01:00:00', 0),
(6, 1, 5, '13:00:00', '01:00:00', 0),
(7, 1, 6, '13:00:00', '01:00:00', 0),
(8, 2, 0, '14:30:00', '22:00:00', 2),
(9, 2, 1, '14:30:00', '22:00:00', 2),
(10, 2, 2, '14:30:00', '22:00:00', 2),
(11, 2, 3, '14:30:00', '22:00:00', 2),
(13, 2, 5, '13:00:00', '01:00:00', 2),
(14, 2, 6, '13:00:00', '01:00:00', 2),
(15, 2, 4, '13:00:00', '01:00:00', 2),
(35, 3, 6, '01:10:00', '01:11:00', 2);

-- --------------------------------------------------------

--
-- Tabellstruktur `ha_log`
--

CREATE TABLE IF NOT EXISTS `ha_log` (
`LogId` int(11) NOT NULL,
  `LogDate` datetime NOT NULL,
  `LogName` varchar(250) NOT NULL,
  `LogLevel` varchar(50) NOT NULL,
  `LogMessage` text NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=2397 DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellstruktur `ha_rooms`
--

CREATE TABLE IF NOT EXISTS `ha_rooms` (
`RoomId` int(11) NOT NULL,
  `RoomName` varchar(255) NOT NULL,
  `RoomDescription` text NOT NULL,
  `RoomOrder` int(11) NOT NULL DEFAULT '100'
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumpning av Data i tabell `ha_rooms`
--

INSERT INTO `ha_rooms` (`RoomId`, `RoomName`, `RoomDescription`, `RoomOrder`) VALUES
(1, 'Vardagsrum', '', 1),
(2, 'Test', 'Test', 2);

-- --------------------------------------------------------

--
-- Tabellstruktur `ha_sensors`
--

CREATE TABLE IF NOT EXISTS `ha_sensors` (
`SensorId` int(11) NOT NULL,
  `SensorRoomId` int(11) DEFAULT NULL,
  `SensorName` varchar(250) NOT NULL,
  `SensorType` varchar(250) NOT NULL,
  `SensorGPIO` int(11) DEFAULT NULL,
  `SensorSerialNo` varchar(250) NOT NULL,
  `SensorOrder` int(11) NOT NULL DEFAULT '100'
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumpning av Data i tabell `ha_sensors`
--

INSERT INTO `ha_sensors` (`SensorId`, `SensorRoomId`, `SensorName`, `SensorType`, `SensorGPIO`, `SensorSerialNo`, `SensorOrder`) VALUES
(1, 1, 'Inomhus', 'DHT22', 9, '', 1),
(2, NULL, 'Utomhus', 'DS18B20', 0, '0000072f3122', 2);

-- --------------------------------------------------------

--
-- Tabellstruktur `ha_sensors_log`
--

CREATE TABLE IF NOT EXISTS `ha_sensors_log` (
`LogId` int(11) NOT NULL,
  `LogSensorId` int(11) NOT NULL,
  `LogDate` datetime NOT NULL,
  `LogValue1` decimal(6,2) DEFAULT NULL,
  `LogValue2` decimal(6,2) DEFAULT NULL,
  `LogValue3` decimal(6,2) DEFAULT NULL,
  `LogValue4` decimal(6,2) DEFAULT NULL,
  `LogValue5` decimal(6,2) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=1485 DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellstruktur `ha_settings`
--

CREATE TABLE IF NOT EXISTS `ha_settings` (
`SettingId` int(11) NOT NULL,
  `SettingName` varchar(250) NOT NULL,
  `SettingValue` varchar(250) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

--
-- Dumpning av Data i tabell `ha_settings`
--

INSERT INTO `ha_settings` (`SettingId`, `SettingName`, `SettingValue`) VALUES
(1, 'Version', 'v0.1.6'),
(2, 'City', 'Gothenburg'),
(3, 'Latitude', '57.70887'),
(4, 'Longitude', '11.97456'),
(5, 'Zenith', '90.83333'),
(6, 'LocalTimeOffset', '1'),
(7, 'WeatherAPIKey', 'dbfa06486fdae1076923fb0d1f12acc9'),
(8, 'SunriseOffset', '0'),
(9, 'SunsetOffset', '-60');

-- --------------------------------------------------------

--
-- Tabellstruktur `ha_user_login`
--

CREATE TABLE IF NOT EXISTS `ha_user_login` (
`Id` int(11) NOT NULL,
  `UserId` int(11) NOT NULL,
  `Date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellstruktur `ha_users`
--

CREATE TABLE IF NOT EXISTS `ha_users` (
`UserId` int(11) NOT NULL,
  `UserName` varchar(30) NOT NULL,
  `UserPassword` varchar(128) NOT NULL,
  `UserMail` varchar(50) NOT NULL,
  `UserSalt` varchar(128) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

--
-- Dumpning av Data i tabell `ha_users`
--

INSERT INTO `ha_users` (`UserId`, `UserName`, `UserPassword`, `UserMail`, `UserSalt`) VALUES
(1, 'admin', 'd5ba1fad157d124551e1b876241d881ab0bb1c504e08ff8a9fe7cbec6a77a861902f4faa02ce2b0a0134d5c349e103ae0c02586d5a6d316c2550d3a967cf1560', 'admin@admin.com', '3a281d1de9ebfe51ccbc96dcab090ca7a8721df675e2249cf8f3f6dfc9c70ecaca5e27c43161879eedd3d559d4a7222dd393a31be8bac81b3118711b1cca25ed');

--
-- Index för dumpade tabeller
--

--
-- Index för tabell `ha_data`
--
ALTER TABLE `ha_data`
 ADD PRIMARY KEY (`DataId`);

--
-- Index för tabell `ha_lamp_objects`
--
ALTER TABLE `ha_lamp_objects`
 ADD PRIMARY KEY (`LampId`), ADD KEY `LampRoomId` (`LampRoomId`);

--
-- Index för tabell `ha_lamp_schedule`
--
ALTER TABLE `ha_lamp_schedule`
 ADD PRIMARY KEY (`ScheduleId`), ADD KEY `ScheduleLampId` (`ScheduleLampId`);

--
-- Index för tabell `ha_log`
--
ALTER TABLE `ha_log`
 ADD PRIMARY KEY (`LogId`);

--
-- Index för tabell `ha_rooms`
--
ALTER TABLE `ha_rooms`
 ADD PRIMARY KEY (`RoomId`);

--
-- Index för tabell `ha_sensors`
--
ALTER TABLE `ha_sensors`
 ADD PRIMARY KEY (`SensorId`), ADD KEY `SensorRoomId` (`SensorRoomId`);

--
-- Index för tabell `ha_sensors_log`
--
ALTER TABLE `ha_sensors_log`
 ADD PRIMARY KEY (`LogId`), ADD KEY `LogSensorId` (`LogSensorId`);

--
-- Index för tabell `ha_settings`
--
ALTER TABLE `ha_settings`
 ADD PRIMARY KEY (`SettingId`);

--
-- Index för tabell `ha_user_login`
--
ALTER TABLE `ha_user_login`
 ADD PRIMARY KEY (`Id`);

--
-- Index för tabell `ha_users`
--
ALTER TABLE `ha_users`
 ADD PRIMARY KEY (`UserId`);

--
-- AUTO_INCREMENT för dumpade tabeller
--

--
-- AUTO_INCREMENT för tabell `ha_data`
--
ALTER TABLE `ha_data`
MODIFY `DataId` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=10000;
--
-- AUTO_INCREMENT för tabell `ha_lamp_objects`
--
ALTER TABLE `ha_lamp_objects`
MODIFY `LampId` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT för tabell `ha_lamp_schedule`
--
ALTER TABLE `ha_lamp_schedule`
MODIFY `ScheduleId` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=40;
--
-- AUTO_INCREMENT för tabell `ha_log`
--
ALTER TABLE `ha_log`
MODIFY `LogId` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2397;
--
-- AUTO_INCREMENT för tabell `ha_rooms`
--
ALTER TABLE `ha_rooms`
MODIFY `RoomId` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT för tabell `ha_sensors`
--
ALTER TABLE `ha_sensors`
MODIFY `SensorId` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT för tabell `ha_sensors_log`
--
ALTER TABLE `ha_sensors_log`
MODIFY `LogId` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=1485;
--
-- AUTO_INCREMENT för tabell `ha_settings`
--
ALTER TABLE `ha_settings`
MODIFY `SettingId` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=10;
--
-- AUTO_INCREMENT för tabell `ha_user_login`
--
ALTER TABLE `ha_user_login`
MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT för tabell `ha_users`
--
ALTER TABLE `ha_users`
MODIFY `UserId` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=16;
--
-- Restriktioner för dumpade tabeller
--

--
-- Restriktioner för tabell `ha_lamp_objects`
--
ALTER TABLE `ha_lamp_objects`
ADD CONSTRAINT `ha_lamp_objects_ibfk_1` FOREIGN KEY (`LampRoomId`) REFERENCES `ha_rooms` (`RoomId`) ON DELETE SET NULL ON UPDATE NO ACTION;

--
-- Restriktioner för tabell `ha_lamp_schedule`
--
ALTER TABLE `ha_lamp_schedule`
ADD CONSTRAINT `ha_lamp_schedule_ibfk_1` FOREIGN KEY (`ScheduleLampId`) REFERENCES `ha_lamp_objects` (`LampId`) ON DELETE CASCADE;

--
-- Restriktioner för tabell `ha_sensors`
--
ALTER TABLE `ha_sensors`
ADD CONSTRAINT `ha_sensors_ibfk_1` FOREIGN KEY (`SensorRoomId`) REFERENCES `ha_rooms` (`RoomId`) ON DELETE SET NULL ON UPDATE NO ACTION;

--
-- Restriktioner för tabell `ha_sensors_log`
--
ALTER TABLE `ha_sensors_log`
ADD CONSTRAINT `ha_sensors_log_ibfk_1` FOREIGN KEY (`LogSensorId`) REFERENCES `ha_sensors` (`SensorId`) ON DELETE CASCADE ON UPDATE NO ACTION;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
