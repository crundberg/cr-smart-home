import time
import logging
import logging.handlers
from datetime import datetime
from Weather import Weather
from Sun import Sun
from Lamp import Lamp
from Config import Config

def main():
	#---------------------------------------------------------------------------# 
	# Logging - Rotate log file at midnight and keep for 30 days
	#---------------------------------------------------------------------------#
	handler = logging.handlers.TimedRotatingFileHandler(Config.Log_Filename, when="midnight", interval=1, backupCount=30)
	handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

	logger = logging.getLogger('home-automation')
	logger.addHandler(handler)
	logger.setLevel(Config.Log_Level)
	
	#---------------------------------------------------------------------------# 
	# Startup
	#---------------------------------------------------------------------------# 
	logger.info('Starting Home Automation %s...' % Config.Version)
	logger.info('System is running in %s (Lat=%f, Long=%f)' % (Config.City, Config.Latitude, Config.Longitude))
	bStartUp = True
	
	#---------------------------------------------------------------------------# 
	# Run program
	#---------------------------------------------------------------------------# 
	weather = Weather()
	sun = Sun()
	lamp = Lamp()

	while True:
		# Update current weather on startup or every 30 minutes
		if (datetime.now().minute == 0 or datetime.now().minute == 30 or bStartUp == True):
			weather.UpdateCurrentWeather();
			
		# Update sun to database every hour
		if (datetime.now().minute == 0 or bStartUp == True):
			sun.UpdateDb()
	
		#Loop through all lamps
		lamp.LoopLampObjects()
		
		#Reset startup bool
		bStartUp = False
		
		#Sleep one minute
		time.sleep(60 - datetime.now().second)

if __name__ == '__main__':
	main()