import time
import logging
import logging.handlers
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
	
	#---------------------------------------------------------------------------# 
	# Run program
	#---------------------------------------------------------------------------# 
	lamp = Lamp()

	while True:
		lamp.LoopLampObjects()
		time.sleep(60)

if __name__ == '__main__':
	main()