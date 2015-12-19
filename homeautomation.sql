-- phpMyAdmin SQL Dump
-- version 4.2.12deb2+deb8u1
-- http://www.phpmyadmin.net
--
-- Värd: localhost
-- Tid vid skapande: 16 dec 2015 kl 18:49
-- Serverversion: 5.5.44-0+deb8u1
-- PHP-version: 5.6.14-0+deb8u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Databas: `homeautomation`
--
CREATE DATABASE IF NOT EXISTS `homeautomation` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `homeautomation`;

--
-- User: `hauser `
--
GRANT USAGE ON *.* TO 'hauser'@'localhost' IDENTIFIED BY PASSWORD '*07BE3499235CA0B7EE65F34EB34DACFE9CFD9942';
GRANT ALL PRIVILEGES ON `homeautomation`.* TO 'hauser'@'localhost' WITH GRANT OPTION;

--
-- Procedurer
--
DROP PROCEDURE IF EXISTS `GetLampSchedulesSimple`;
DELIMITER $$
CREATE PROCEDURE `GetLampSchedulesSimple` ()
BEGIN
SELECT t3.LampId, t3.LampName, t3.LampIO, t3.LampPowerOn, t3.LampCmdOn, t3.LampCmdOff, t1.ScheduleWeekday, t1.ScheduleTimeOn, t1.ScheduleTimeOff, t1.ScheduleMode
FROM ha_lamp_objects t3
LEFT JOIN ha_lamp_schedule t1 on t1.ScheduleLampId = t3.LampId
WHERE t1.ScheduleWeekday = WEEKDAY(NOW()) OR t1.ScheduleWeekday = WEEKDAY(DATE_SUB(NOW(), INTERVAL 1 DAY))
ORDER BY t3.LampId;
END $$
DELIMITER ;

-- --------------------------------------------------------

--
-- Tabellstruktur `ha_lamp_objects`
--

DROP TABLE IF EXISTS `ha_lamp_objects`;
CREATE TABLE `ha_lamp_objects` (
`LampId` int(11) NOT NULL,
  `LampName` varchar(255) NOT NULL,
  `LampIO` varchar(255) NOT NULL,
  `LampType` varchar(255) NOT NULL,
  `LampPowerOn` tinyint(2) NOT NULL,
  `LampPowerOnMan` tinyint(2) NOT NULL,
  `LampCmdOn` varchar(255) NOT NULL,
  `LampCmdOff` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellstruktur `ha_lamp_schedule`
--

DROP TABLE IF EXISTS `ha_lamp_schedule`;
CREATE TABLE `ha_lamp_schedule` (
`ScheduleId` int(11) NOT NULL,
  `ScheduleLampId` int(11) NOT NULL,
  `ScheduleWeekday` int(11) NOT NULL,
  `ScheduleTimeOn` time NOT NULL,
  `ScheduleTimeOff` time NOT NULL,
  `ScheduleMode` int(11) NOT NULL DEFAULT '0' COMMENT '0=Inactive, 1=On, 2=On if sun is down'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellstruktur `ha_users`
--

DROP TABLE IF EXISTS `ha_users`;
CREATE TABLE `ha_users` (
`UserId` int(11) NOT NULL,
  `UserName` varchar(30) NOT NULL,
  `UserPassword` varchar(128) NOT NULL,
  `UserMail` varchar(50) NOT NULL,
  `UserSalt` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumpning av Data i tabell `ha_users`
--

INSERT INTO `ha_users` (`UserId`, `UserName`, `UserPassword`, `UserMail`, `UserSalt`) VALUES
(1, 'admin', 'd5ba1fad157d124551e1b876241d881ab0bb1c504e08ff8a9fe7cbec6a77a861902f4faa02ce2b0a0134d5c349e103ae0c02586d5a6d316c2550d3a967cf1560', 'admin', '3a281d1de9ebfe51ccbc96dcab090ca7a8721df675e2249cf8f3f6dfc9c70ecaca5e27c43161879eedd3d559d4a7222dd393a31be8bac81b3118711b1cca25ed');

-- --------------------------------------------------------

--
-- Tabellstruktur `ha_user_login`
--

DROP TABLE IF EXISTS `ha_user_login`;
CREATE TABLE IF NOT EXISTS `ha_user_login` (
  `Id` int(11) NOT NULL,
  `UserId` int(11) NOT NULL,
  `Date` datetime NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

--
-- Index för dumpade tabeller
--

--
-- Index för tabell `ha_lamp_objects`
--
ALTER TABLE `ha_lamp_objects`
 ADD PRIMARY KEY (`LampId`);

--
-- Index för tabell `ha_lamp_schedule`
--
ALTER TABLE `ha_lamp_schedule`
 ADD PRIMARY KEY (`ScheduleId`), ADD KEY `ScheduleLampId` (`ScheduleLampId`);

--
-- Index för tabell `ha_users`
--
ALTER TABLE `ha_users`
 ADD PRIMARY KEY (`UserId`);

--
-- Index för tabell `ha_user_login`
--
ALTER TABLE `ha_user_login`
 ADD PRIMARY KEY (`Id`);

--
-- AUTO_INCREMENT för dumpade tabeller
--

--
-- AUTO_INCREMENT för tabell `ha_lamp_objects`
--
ALTER TABLE `ha_lamp_objects`
MODIFY `LampId` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT för tabell `ha_lamp_schedule`
--
ALTER TABLE `ha_lamp_schedule`
MODIFY `ScheduleId` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT för tabell `ha_users`
--
ALTER TABLE `ha_users`
MODIFY `UserId` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT för tabell `ha_user_login`
--
ALTER TABLE `ha_user_login`
MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restriktioner för dumpade tabeller
--

--
-- Restriktioner för tabell `ha_lamp_schedule`
--
ALTER TABLE `ha_lamp_schedule`
ADD CONSTRAINT `ha_lamp_schedule_ibfk_1` FOREIGN KEY (`ScheduleLampId`) REFERENCES `ha_lamp_objects` (`LampId`) ON DELETE CASCADE;
