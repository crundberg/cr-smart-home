# Based on SunriseSunsetCalculator by jebeaudet
# https://github.com/jebeaudet/SunriseSunsetCalculator

import math
import datetime
import time
import MySQLdb
from Config import Config
from Log import Log

class Sun:
	#---------------------------------------------------------------------------# 
	# Constructor
	#---------------------------------------------------------------------------# 
	def __init__(self):
		self.log = Log()
		self.zenith = 0
		self.localOffset = 0
		self.latitude = 0
		self.longitude = 0
		self.GetSettings()
		
		if self.latitude < -90 or self.latitude > 90:
			self.log.error('Server', 'Invalid latitude value')
		if self.longitude < -180 or self.longitude > 180:
			self.log.error('Server', 'Invalid longitude value')
		if self.localOffset < -12 or self.localOffset > 14:
			self.log.error('Server', 'Invalid local time offset value')
		if self.zenith == 0:
			self.log.error('Server', 'Invalid zenith value')
        

	#---------------------------------------------------------------------------# 
	# Sun is down
	#---------------------------------------------------------------------------# 	
	def sunIsDown(self):
		now = datetime.datetime.now()
 		sunrise = self.sunrise(now, self.latitude, self.longitude)
 		sunset = self.sunset(now, self.latitude, self.longitude)
		return (now < sunrise or now > sunset)
		
	#---------------------------------------------------------------------------# 
	# Sun is up
	#---------------------------------------------------------------------------# 	
	def sunIsUp(self):
		now = datetime.datetime.now()
 		sunrise = self.sunrise(now, self.latitude, self.longitude)
 		sunset = self.sunset(now, self.latitude, self.longitude)
		return (now > sunrise or now < sunset)
		
	#---------------------------------------------------------------------------# 
	# Update to database
	#---------------------------------------------------------------------------# 	
	def UpdateDb(self):
		now = datetime.datetime.now()
 		sunrise = self.sunrise(now, self.latitude, self.longitude)
 		sunset = self.sunset(now, self.latitude, self.longitude)
 		
 		data = '{"Sunrise":"%s","Sunset":"%s"}' % (sunrise, sunset) 		
 		sql = "INSERT INTO ha_data (DataId, DataName, DataText, DataStatus, DataLastUpdated) VALUES (3, 'Sun', '%s', 200, NOW()) ON DUPLICATE KEY UPDATE DataText = VALUES(DataText), DataStatus = VALUES(DataStatus), DataLastUpdated = VALUES(DataLastUpdated)" % data
		
		self.SQLQuery(sql)
	
	#---------------------------------------------------------------------------# 
	# Adjust angle
	#---------------------------------------------------------------------------# 
	def adjustAngle(self, L):
	    if L < 0:
	        return L + 360
	    elif L >= 360:
	        return L - 360
	    return L
	
	#---------------------------------------------------------------------------# 
	# Adjust function
	#---------------------------------------------------------------------------# 
	def adjustTime(self, L):
	    if L < 0:
	        return L + 24
	    elif L >= 24:
	        return L - 24
	    return L
	
	#---------------------------------------------------------------------------# 
	# Get sunrise
	#---------------------------------------------------------------------------# 
	def sunrise(self, date, latitude, longitude):
		#Date
		day = date.day
		month = date.month
		year = date.year
	
		#Calculate the day of the year
		N1 = math.floor(275 * month / 9)
		N2 = math.floor((month + 9) / 12)
		N3 = (1 + math.floor((year - 4 * math.floor(year / 4) + 2) / 3))
		N = N1 - (N2 * N3) + day - 30
	
		#Convert the longitude to hour value and calculate an approximate time
		lngHour = longitude / 15
		t_rise = N + ((6 - lngHour) / 24)
	
		#Calculate the Sun's mean anomaly
		M_rise = (0.9856 * t_rise) - 3.289
	
		#Calculate the Sun's true longitude
		L_rise = self.adjustAngle(M_rise + (1.916 * math.sin(math.radians(M_rise))) + (0.020 * math.sin(math.radians(2 * M_rise))) + 282.634)
	
		#Calculate the Sun's right ascension
		RA_rise = self.adjustAngle(math.degrees(math.atan(0.91764 * math.tan(math.radians(L_rise)))))
	
		#Right ascension value needs to be in the same quadrant as L
		Lquadrant_rise  = (math.floor(L_rise/90)) * 90
		RAquadrant_rise = (math.floor(RA_rise/90)) * 90
		RA_rise = RA_rise + (Lquadrant_rise - RAquadrant_rise)
	
		#Right ascension value needs to be converted into hours
		RA_rise = RA_rise / 15
	
		#Calculate the Sun's declination
		sinDec_rise = 0.39782 * math.sin(math.radians(L_rise))
		cosDec_rise = math.cos(math.asin(sinDec_rise))
	
		#Calculate the Sun's local hour angle
		cosH_rise = (math.cos(math.radians(self.zenith)) - (sinDec_rise * math.sin(math.radians(latitude)))) / (cosDec_rise * math.cos(math.radians(latitude)))
	
		#Finish calculating H and convert into hours
		H_rise = (360 - math.degrees(math.acos(cosH_rise))) / 15
	
		#Calculate local mean time of rising/setting
		T_rise = H_rise + RA_rise - (0.06571 * t_rise) - 6.622
	
		#Adjust back to UTC
		UT_rise = self.adjustTime(T_rise - lngHour)
	
		#Convert UT value to local time zone of latitude/longitude
		localT_rise = self.adjustTime(UT_rise + self.localOffset)
	
		#Conversion
		h_rise = int(localT_rise)
		m_rise = int(localT_rise % 1 * 60)
	
		#Return
		return datetime.datetime(year, month, day, h_rise, m_rise)
	
	#---------------------------------------------------------------------------# 
	# Get sunset
	#---------------------------------------------------------------------------# 
	def sunset(self, date, latitude, longitude):
		#Date
		day = date.day
		month = date.month
		year = date.year
	
		#Calculate the day of the year
		N1 = math.floor(275 * month / 9)
		N2 = math.floor((month + 9) / 12)
		N3 = (1 + math.floor((year - 4 * math.floor(year / 4) + 2) / 3))
		N = N1 - (N2 * N3) + day - 30
	
		#Convert the longitude to hour value and calculate an approximate time
		lngHour = longitude / 15
		t_set = N + ((18 - lngHour) / 24)
	
		#Calculate the Sun's mean anomaly
		M_set = (0.9856 * t_set) - 3.289
	
		#Calculate the Sun's true longitude
		L_set = self.adjustAngle(M_set + (1.916 * math.sin(math.radians(M_set))) + (0.020 * math.sin(math.radians(2 * M_set))) + 282.634)
	
		#Calculate the Sun's right ascension
		RA_set = self.adjustAngle(math.degrees(math.atan(0.91764 * math.tan(math.radians(L_set)))))
	
		#Right ascension value needs to be in the same quadrant as L
		Lquadrant_set  = (math.floor(L_set/90)) * 90
		RAquadrant_set = (math.floor(RA_set/90)) * 90
		RA_set = RA_set + (Lquadrant_set - RAquadrant_set)
	
		#Right ascension value needs to be converted into hours
		RA_set = RA_set / 15
	
		#Calculate the Sun's declination
		sinDec_set = 0.39782 * math.sin(math.radians(L_set))
		cosDec_set = math.cos(math.asin(sinDec_set))
	
		#Calculate the Sun's local hour angle
		cosH_set = (math.cos(math.radians(self.zenith)) - (sinDec_set * math.sin(math.radians(latitude)))) / (cosDec_set * math.cos(math.radians(latitude)))
	
		#Finish calculating H and convert into hours
		H_set = math.degrees(math.acos(cosH_set)) / 15
	
		#Calculate local mean time of rising/setting
		T_set = H_set + RA_set - (0.06571 * t_set) - 6.622
	
		#Adjust back to UTC
		UT_set = self.adjustTime(T_set - lngHour)
	
		#Convert UT value to local time zone of latitude/longitude
		localT_set = self.adjustTime(UT_set + self.localOffset)
	
		#Conversion
		h_set = int(localT_set)
		m_set = int(localT_set % 1 * 60)
	
		#Return
		return datetime.datetime(year, month, day, h_set, m_set)
		
	#---------------------------------------------------------------------------# 
	# Get settings
	#---------------------------------------------------------------------------# 
	def GetSettings(self):
		#Connect to MySQL
		db = MySQLdb.connect(Config.DbHost, Config.DbUser, Config.DbPassword, Config.DbName)
		cursor = db.cursor()
	
		try:
			#Execure SQL-Query
			cursor.execute("SELECT SettingName, SettingValue FROM ha_settings WHERE SettingName='Latitude' OR SettingName='Longitude' OR SettingName='Zenith' OR SettingName='LocalTimeOffset'")
			results = cursor.fetchall()
		
			#Loop result from database
			for row in results:					
				#Move database row to variables
				if (row[0] == 'Latitude'):
					self.latitude = float(row[1])
				elif (row[0] == 'Longitude'):
					self.longitude = float(row[1])
				elif (row[0] == 'Zenith'):
					self.zenith = float(row[1])
				elif (row[0] == 'LocalTimeOffset'):
					self.localOffset = int(row[1])
	
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