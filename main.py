import time
import Lamp
from Config import Config

#---------------------------------------------------------------------------# 
# Startup
#---------------------------------------------------------------------------# 
print 'Starting Home Automation %s...' % Config.Version
print 'System is running in %s (Lat=%f, Long=%f)' % (Config.City, Config.Latitude, Config.Longitude)
print ''

#---------------------------------------------------------------------------# 
# Run program
#---------------------------------------------------------------------------# 
while True:
	Lamp.LoopLampObjects()
	time.sleep(60)