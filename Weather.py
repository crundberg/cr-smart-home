import requests
import json
import MySQLdb
import sys
from Config import Config
from Log import Log

class Weather:
	#---------------------------------------------------------------------------# 
	# Constructor
	#---------------------------------------------------------------------------# 
	def __init__(self):
		self.log = Log()
		self.apikey = ''
		self.city = ''
		self.GetSettings()

	#---------------------------------------------------------------------------# 
	# Get current weather
	#---------------------------------------------------------------------------# 
	def UpdateCurrentWeather(self):
		#Return if no API key is entered in Config
		if (self.apikey == ""):
			return
			
		# Get weather from OpenWeatherMap
		url = 'http://api.openweathermap.org/data/2.5/find?q=%s&units=metric&appid=%s' % (self.city, self.apikey)
		
		try:
			response = requests.get(url)
		
			# If status isn't OK
			if response.status_code == 200:
				#Update database
				self.SQLQuery("UPDATE ha_data SET DataText = '%s', DataStatus = '%s', DataLastUpdated = NOW() WHERE DataName = 'Weather'" % (response.text, response.status_code))
			else:
				self.log.error('Server', 'Weather API: Status Code %s' % response.status_code)
		except requests.exceptions.RequestException as e:
			self.log.error('Server', 'Weather Error: %s' % e)
		except:
			self.log.error('Server', 'Unexpected weather error: %s' % sys.exc_info()[0])
			
	#---------------------------------------------------------------------------# 
	# Get settings
	#---------------------------------------------------------------------------# 
	def GetSettings(self):
		#Connect to MySQL
		db = MySQLdb.connect(Config.DbHost, Config.DbUser, Config.DbPassword, Config.DbName)
		cursor = db.cursor()
	
		try:
			#Execure SQL-Query
			cursor.execute("SELECT SettingName, SettingValue FROM ha_settings WHERE SettingName='City' OR SettingName='WeatherAPIKey'")
			results = cursor.fetchall()
		
			#Loop result from database
			for row in results:					
				#Move database row to variables
				if (row[0] == 'City'):
					self.city = row[1]
				elif (row[0] == 'WeatherAPIKey'):
					self.apikey = row[1]
	
		except MySQLdb.Error, e:
			#Log exceptions
			try:
				self.log.error('Server', 'MySQL Error [%d]: %s' % (e.args[0], e.args[1]))
	
			except IndexError:
				self.log.error('Server', 'MySQL Error: %s' % str(e))
		finally:
			#Close database connection
			cursor.close()
			db.close()

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
			self.log.error('Server', 'MySQL Error [%d]: %s' % (e.args[0], e.args[1]))
		except:
			self.log.error('Server', 'Unexpected error: %s' % (sys.exc_info()[0]))
		finally:
			cursor.close()
			db.close()