import datetime
import time
import SunriseSunset
import LampClass

#Parameters
version = 'v0.1'	#Version of program
city = 'Goteborg'	#City
latitude = 57.70887	#Latitude for Goteborg
longitude = 11.97456	#Longitude for Goteborg

#Lamp objects
lamp1 = LampClass.Lamp("Hall", "IO1", "15:00", "23:00", 0)
lamp2 = LampClass.Lamp("Vardagsrum", "IO2", "15:00", "01:00", 1)
lamp3 = LampClass.Lamp("Sovrum", "IO3", "15:00", "01:00", 1)
LampObjects = [lamp1, lamp2,  lamp3]

#Startup
print 'Starting Home Automation %s...' % version
print 'System is running in %s (Lat=%f, Long=%f)' % (city, latitude, longitude)
print ''

#Print objects
if (LampClass.Lamp.LampCount == 0):
	print 'No objects configured'
else:
	print 'Configured lamps:'

n = 0

for lamp in LampObjects:
	n+=1
	print '%d: %s (%s), Start: %s, Stop: %s, Active: %d' % (n, lamp.Name, lamp.IO, lamp.TimeStart, lamp.TimeStop, lamp.Active)

#Run program
while True:
	#Datetime
	now = datetime.datetime.now()
	sunset = SunriseSunset.sunset(now, latitude, longitude)
	sunrise = SunriseSunset.sunrise(now, latitude, longitude)
	dark = (now < sunrise or now > sunset)

	print ''
	print 'Time: %02d:%02d, Dark: %d, Sunset: %s, Sunrise: %s' % (now.hour, now.minute, dark, sunset, sunrise)

	#Loop objects
	for lamp in LampObjects:
		#Start and stop time for lamp
		sStart = '%s %s' % (now.date(), lamp.TimeStart)
		sStop = '%s %s' % (now.date(), lamp.TimeStop)
		dtStart = datetime.datetime.strptime(sStart, '%Y-%m-%d %H:%M')
		dtStop = datetime.datetime.strptime(sStop, '%Y-%m-%d %H:%M')

		if (dtStart > dtStop):
			dtStop += datetime.timedelta(days=1)

		bStart = (now > dtStart and now < dtStop)

		#Object inactive
		if (lamp.Active == 0):
			print '%s is inactivate' % lamp.Name
			continue
		
		#Start lamp
		if (bStart and dark):
			if (lamp.Started == 0):
				print 'Starting %s' % lamp.Name
				lamp.Started = 1
				continue
			else:
				print '%s is already started' % lamp.Name
				lamp.Started = 1
				continue	

		#Stop lamp
		if (not bStart or not dark):
			if (lamp.Started == 1):
				print 'Stoping %s' % lamp.Name
				lamp.Started = 0
				continue
			else:
				print '%s is already stoped' % lamp.Name
				lamp.Started = 0
				continue

	#Sleep 60s
	time.sleep(60)
