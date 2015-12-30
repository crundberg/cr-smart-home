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
		self.Version = "v0.1.2"
	

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
				self.SQLQuery("ALTER TABLE `ha_settings` CHANGE `SettingId` `SettingId` INT( 11 ) NOT NULL AUTO_INCREMENT; INSERT INTO ha_settings (SettingId, SettingName, SettingValue) VALUES (NULL, 'City', 'Gothenburg'), (NULL, 'Latitude', '57.70887'), (NULL, 'Longitude', '11.97456'), (NULL, 'Zenith', '90.83333'), (NULL, 'LocalTimeOffset', '1'), (NULL, 'WeatherAPIKey', '')")
			
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