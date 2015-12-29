import requests
import json
import logging
import MySQLdb
import sys
from Config import Config
from Log import Log

log = Log()
logger = logging.getLogger('home-automation')

class Weather:
	#---------------------------------------------------------------------------# 
	# Constructor
	#---------------------------------------------------------------------------# 
	def __init__(self):
		self.apikey = Config.WeatherAPIKey
		self.city = Config.City

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
				log.error('Server', 'Weather API: Status Code %s' % response.status_code)
		except requests.exceptions.RequestException as e:
			log.error('Server', 'Weather Error: %s' % e)
		except:
			log.error('Server', 'Unexpected weather error: %s' % sys.exc_info()[0])

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
				log.error('Server', 'MySQL Error [%d]: %s' % (e.args[0], e.args[1]))
			except:
				log.error('Server', 'Unexpected error: %s' % (sys.exc_info()[0]))
			finally:
				cursor.close()
				db.close()