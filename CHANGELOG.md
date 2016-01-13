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

## 2016-01-03
Changed project name, run the following SQL-queries.
```
RENAME DATABASE homeautomation TO crsmarthome;
GRANT ALL PRIVILEGES ON `crsmarthome`.* TO 'hauser'@'localhost' WITH GRANT OPTION;
```

Open configuration file for Apache `sudo nano /etc/apache2/sites-available/000-default.conf`
Find the row `DocumentRoot /home/pi/Documents/home-automation-webgui` and replace it with `DocumentRoot /home/pi/Documents/cr-smart-home-webgui`.
Find the row `<Directory /home/pi/Documents/home-automation-webgui/ >` and replace it with `<Directory /home/pi/Documents/cr-smart-home-webgui/ >`.

Upgrade autostart file
```
sudo /etc/init.d/homeautomation stop
sudo update-rc.d [-f] homeautomation remove
sudo cp /home/pi/Documents/cr-smart-home/autostart/crsmarthome /etc/init.d/
sudo chmod +x /etc/init.d/crsmarthome
sudo update-rc.d crsmarthome defaults
sudo /etc/init.d/crsmarthome start
```

## 2016-01-12
Updated autostart script, run the following commands in Terminal
```
sudo update-rc.d -f crsmarthome remove
sudo cp /home/pi/Documents/cr-smart-home/autostart/crsmarthome /etc/init.d/
sudo chmod +x /etc/init.d/crsmarthome
sudo update-rc.d crsmarthome defaults
```

Run this command `ls -l /etc/rc?.d/*crsmarthome` and verify it looks like this:
```
lrwxrwxrwx 1 root root 21 Jan 12 13:15 /etc/rc0.d/K01crsmarthome -> ../init.d/crsmarthome
lrwxrwxrwx 1 root root 21 Jan 12 13:15 /etc/rc1.d/K01crsmarthome -> ../init.d/crsmarthome
lrwxrwxrwx 1 root root 21 Jan 12 13:15 /etc/rc2.d/S04crsmarthome -> ../init.d/crsmarthome
lrwxrwxrwx 1 root root 21 Jan 12 13:15 /etc/rc3.d/S04crsmarthome -> ../init.d/crsmarthome
lrwxrwxrwx 1 root root 21 Jan 12 13:15 /etc/rc4.d/S04crsmarthome -> ../init.d/crsmarthome
lrwxrwxrwx 1 root root 21 Jan 12 13:15 /etc/rc5.d/S04crsmarthome -> ../init.d/crsmarthome
lrwxrwxrwx 1 root root 21 Jan 12 13:15 /etc/rc6.d/K01crsmarthome -> ../init.d/crsmarthome

```

## 2016-01-13
Added support for temperaturesensors. Install Adafruit DHT library with the follwing commands
```
sudo apt-get update
sudo apt-get install build-essential python-dev python-openssl

cd /home/pi/Documents
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo python setup.py install

sudo apt-get install python3-w1thermsensor
```