import time
import logging
import logging.handlers
from datetime import datetime
from Weather import Weather
from Sun import Sun
from Lamp import Lamp
from Config import Config
from Log import Log
from Upgrade import Upgrade

def main():
	#---------------------------------------------------------------------------# 
	# Logging - Rotate log file at midnight and keep for 7 days
	#---------------------------------------------------------------------------#	
	handler = logging.handlers.TimedRotatingFileHandler(Config.Log_Filename, when="midnight", interval=1, backupCount=7)
	handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

	logger = logging.getLogger('cr-smart-home')
	logger.addHandler(handler)
	logger.setLevel(Config.Log_Level)
	
	log = Log()
	log.info('Server', 'Starting CR Smart Home %s...' % Config.Version)

	#---------------------------------------------------------------------------# 
	# Upgrade
	#---------------------------------------------------------------------------#	
	upgrade = Upgrade()
	upgrade.Upgrade()
	
	#---------------------------------------------------------------------------# 
	# Startup
	#---------------------------------------------------------------------------#
	weather = Weather()
	sun = Sun()
	lamp = Lamp()
	
	log.info('Server', 'System is running in %s (Lat=%f, Long=%f)' % (weather.city, sun.latitude, sun.longitude))
	bStartUp = True
	
	#---------------------------------------------------------------------------# 
	# Run program
	#---------------------------------------------------------------------------# 
	while True:
		# Update current weather on startup or every 30 minutes
		if (datetime.now().minute == 0 or datetime.now().minute == 30 or bStartUp == True):
			weather.UpdateCurrentWeather();
			
		# Update sun to database every hour
		if (datetime.now().minute == 0 or bStartUp == True):
			sun.UpdateDb()
	
		#Loop through all lamps
		lamp.Schedule()
		
		#Reset startup bool
		bStartUp = False

		#Sleep one minute
		time.sleep(60 - datetime.now().second)

if __name__ == '__main__':
	main()