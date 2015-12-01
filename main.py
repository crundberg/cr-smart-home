import datetime
import time
import MySQLdb
import SunriseSunset
import Lamp

#Parameters
version = 'v0.1'	#Version of program
city = 'Goteborg'	#City
latitude = 57.70887	#Latitude for Goteborg
longitude = 11.97456	#Longitude for Goteborg

#Startup
print 'Starting Home Automation %s...' % version
print 'System is running in %s (Lat=%f, Long=%f)' % (city, latitude, longitude)
print ''

#Run program
while True:
	#Loop lamp obects
	Lamp.LoopLampObjects()

	#Sleep 60s
	time.sleep(60)
