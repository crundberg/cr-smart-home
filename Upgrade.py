import requests
import json
import MySQLdb
import sys
import re
from Config import Config
from Log import Log

class Upgrade:
	#---------------------------------------------------------------------------# 
	# Constructor
	#---------------------------------------------------------------------------# 
	def __init__(self):
		self.log = Log()
		self.error = 0
		self.Version = "v0.1.6"
	

	#---------------------------------------------------------------------------# 
	# Get current version
	#---------------------------------------------------------------------------# 
	def GetCurrentVersion(self):
		version = "v0.0"
		
		#Connect to MySQL
		db = MySQLdb.connect(Config.DbHost, Config.DbUser, Config.DbPassword, Config.DbName)
		cursor = db.cursor()
	
		try:
			#Execure SQL-Query
			cursor.execute("SELECT SettingValue FROM ha_settings WHERE SettingName='Version'")
			result = cursor.fetchone()
			version = result[0]
		except MySQLdb.Error, e:
			#Log exceptions
			try:
				self.error = 1
				self.log.error('Server', 'MySQL Error [%d]: %s' % (e.args[0], e.args[1]))
	
			except IndexError:
				self.error = 1
				self.log.error('Server', 'MySQL Error: %s' % str(e))
		finally:
			#Close database connection
			cursor.close()
			db.close()
		
		return version
	

	#---------------------------------------------------------------------------# 
	# Version to int
	#---------------------------------------------------------------------------# 
	def VersionToInt(self, v):
		return [int(x) for x in re.sub(r'[^\d.]+','', v).split(".")]
		
	#---------------------------------------------------------------------------# 
	# Upgrade
	#---------------------------------------------------------------------------# 
	def Upgrade(self):
		dbVersion = self.GetCurrentVersion()
		
		# Program is up to date
		if (cmp(self.VersionToInt(self.Version), self.VersionToInt(dbVersion)) <> 0):
			# Upgrade to v0.1.1
			if (cmp(self.VersionToInt("v0.1.1"), self.VersionToInt(dbVersion)) > 0):
				self.log.info("Server", "Start upgrading to v0.1.1")

			# Upgrade to v0.1.2
			if (cmp(self.VersionToInt("v0.1.2"), self.VersionToInt(dbVersion)) > 0):
				self.log.info("Server", "Start upgrading to v0.1.2")
				self.SQLQuery("ALTER TABLE `ha_settings` CHANGE `SettingId` `SettingId` INT( 11 ) NOT NULL AUTO_INCREMENT")
				self.SQLQuery("INSERT INTO ha_settings (SettingId, SettingName, SettingValue) VALUES (NULL, 'City', 'Gothenburg'), (NULL, 'Latitude', '57.70887'), (NULL, 'Longitude', '11.97456'), (NULL, 'Zenith', '90.83333'), (NULL, 'LocalTimeOffset', '1'), (NULL, 'WeatherAPIKey', '')")

			# Upgrade to v0.1.3
			if (cmp(self.VersionToInt("v0.1.3"), self.VersionToInt(dbVersion)) > 0):
				self.log.info("Server", "Start upgrading to v0.1.3")
				self.SQLQuery("CREATE TABLE `ha_rooms` (`RoomId` int(11) NOT NULL DEFAULT '0', `RoomName` varchar(255) NOT NULL, `RoomDescription` text NOT NULL, `RoomOrder` int(11) NOT NULL DEFAULT '100') ENGINE=InnoDB DEFAULT CHARSET=latin1")
				self.SQLQuery("ALTER TABLE `ha_rooms` ADD PRIMARY KEY (`RoomId`)")
				self.SQLQuery("ALTER TABLE `ha_rooms` MODIFY `RoomId` int(11) NOT NULL AUTO_INCREMENT")
				self.SQLQuery("ALTER TABLE `ha_lamp_objects` ADD `LampRoomId` INT(11) NULL AFTER `LampId`, ADD INDEX (`LampRoomId`)")
				self.SQLQuery("ALTER TABLE `ha_lamp_objects` ADD FOREIGN KEY (`LampRoomId`) REFERENCES `homeautomation`.`ha_rooms`(`RoomId`) ON DELETE SET NULL ON UPDATE NO ACTION")

			# Upgrade to v0.1.4
			if (cmp(self.VersionToInt("v0.1.4"), self.VersionToInt(dbVersion)) > 0):
				self.log.info("Server", "Start upgrading to v0.1.4")

			# Upgrade to v0.1.5
			if (cmp(self.VersionToInt("v0.1.5"), self.VersionToInt(dbVersion)) > 0):				
				self.SQLQuery("INSERT INTO `ha_settings` (`SettingId`, `SettingName`, `SettingValue`) VALUES (NULL, 'SunriseOffset', '0'), (NULL, 'SunsetOffset', '0');")

			# Upgrade to v0.1.6
			if (cmp(self.VersionToInt("v0.1.6"), self.VersionToInt(dbVersion)) > 0):				
				self.SQLQuery("CREATE TABLE `ha_sensors` (`SensorId` int(11) NOT NULL, `SensorRoomId` int(11) DEFAULT NULL, `SensorName` varchar(250) NOT NULL, `SensorType` varchar(250) NOT NULL, `SensorGPIO` int(11) DEFAULT NULL, `SensorSerialNo` varchar(250) NOT NULL, `SensorOrder` int(11) NOT NULL DEFAULT '100') ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;")
				self.SQLQuery("CREATE TABLE `ha_sensors_log` (`LogId` int(11) NOT NULL, `LogSensorId` int(11) NOT NULL, `LogDate` datetime NOT NULL, `LogValue1` decimal(6,2) DEFAULT NULL, `LogValue2` decimal(6,2) DEFAULT NULL, `LogValue3` decimal(6,2) DEFAULT NULL, `LogValue4` decimal(6,2) DEFAULT NULL, `LogValue5` decimal(6,2) DEFAULT NULL) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;")
				self.SQLQuery("ALTER TABLE `ha_sensors` ADD PRIMARY KEY (`SensorId`), ADD KEY `SensorRoomId` (`SensorRoomId`);")
				self.SQLQuery("ALTER TABLE `ha_sensors_log` ADD PRIMARY KEY (`LogId`), ADD KEY `LogSensorId` (`LogSensorId`);")
				self.SQLQuery("ALTER TABLE `ha_sensors` MODIFY `SensorId` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=1;")
				self.SQLQuery("ALTER TABLE `ha_sensors_log` MODIFY `LogId` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=46;")
				self.SQLQuery("ALTER TABLE `ha_sensors` ADD CONSTRAINT `ha_sensors_ibfk_1` FOREIGN KEY (`SensorRoomId`) REFERENCES `ha_rooms` (`RoomId`) ON DELETE SET NULL ON UPDATE NO ACTION;")
				self.SQLQuery("ALTER TABLE `ha_sensors_log` ADD CONSTRAINT `ha_sensors_log_ibfk_1` FOREIGN KEY (`LogSensorId`) REFERENCES `ha_sensors` (`SensorId`) ON DELETE CASCADE ON UPDATE NO ACTION;")
			
			# Upgrade finished
			if (self.error == 0):
				self.SQLQuery("UPDATE ha_settings SET SettingValue='%s' WHERE SettingName='Version'" % self.Version)
				self.log.info("Server", "Upgrading finished successfully!")
			else:
				self.log.error("Server", "Upgrading finished with errors!")			
	

	#---------------------------------------------------------------------------# 
	# SQL Query
	#---------------------------------------------------------------------------# 			
	def SQLQuery(self, sSQL):
			db = MySQLdb.connect(Config.DbHost, Config.DbUser, Config.DbPassword, Config.DbName)
			cursor = db.cursor()
		
			try:
				cursor.execute(sSQL)
				db.commit()
			except MySQLdb.Error, e:
				db.rollback()
				self.error = 1
				self.log.error('Server', 'MySQL Error [%d]: %s' % (e.args[0], e.args[1]))
			except:
				self.error = 1
				self.log.error('Server', 'Unexpected error: %s' % (sys.exc_info()[0]))
			finally:
				cursor.close()
				db.close()