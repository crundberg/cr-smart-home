#!/usr/bin/python

import MySQLdb
import Adafruit_DHT
from Config import Config
from Log import Log
from w1thermsensor import W1ThermSensor, NoSensorFoundError, SensorNotReadyError, UnsupportedUnitError

class Sensor:
	#---------------------------------------------------------------------------# 
	# Constructor
	#---------------------------------------------------------------------------# 
	def __init__(self):
		self.log = Log()

	#---------------------------------------------------------------------------# 
	# DHTxx sensors
	#---------------------------------------------------------------------------# 
	def DHT(self, Id, SensorType, GPIO):

		humidity, temperature = Adafruit_DHT.read_retry(SensorType, GPIO)

		if humidity is not None and temperature is not None:
			self.SQLQuery("INSERT INTO ha_sensors_log (LogSensorId, LogDate, LogValue1, LogValue2) VALUES ('%s', NOW(), '%.2f', '%.2f')" % (Id, temperature, humidity))
		else:
			self.log.warning('Server', 'Failed to get reading. Try again!')

	#---------------------------------------------------------------------------# 
	# DSxx sensors
	#---------------------------------------------------------------------------# 
	def DS(self, Id, SensorType, SerialNo):

		try:
			sensor = W1ThermSensor(SensorType, SerialNo)
			temperature = sensor.get_temperature()
		except (UnsupportedUnitError, NoSensorFoundError, SensorNotReadyError) as e:
			self.log.error('Server', 'Sensor Error: %s' % str(e).replace("'", '"'))
			return
		
		
		
		if temperature is not None:
			self.SQLQuery("INSERT INTO ha_sensors_log (LogSensorId, LogDate, LogValue1) VALUES ('%s', NOW(), '%.2f')" % (Id, temperature))
		else:
			self.log.warning('Server', 'Failed to get reading. Try again!')

	#---------------------------------------------------------------------------# 
	# Read all sensors
	#---------------------------------------------------------------------------# 
	def readAll(self):
		# Connect to database
		db = MySQLdb.connect(Config.DbHost, Config.DbUser, Config.DbPassword, Config.DbName)
		cursor = db.cursor()
		
		try:
			# Select lamps from database
			cursor.execute("SELECT SensorId, SensorName, SensorType, SensorGPIO, SensorSerialNo FROM ha_sensors ORDER BY SensorId ASC")
			results = cursor.fetchall()
		
			# Loop result from database
			for row in results:
				# Move result to variables
				dbId = row[0]
				dbName = row[1]
				dbType = row[2]
				dbGPIO = row[3]
				dbSerialNo = row[4]
			
				if (dbType == "DHT11"):
					self.DHT(dbId, Adafruit_DHT.DHT11, dbGPIO)
				elif (dbType == "DHT22"):
					self.DHT(dbId, Adafruit_DHT.DHT22, dbGPIO)
				elif (dbType == "AM2302"):
					self.DHT(dbId, Adafruit_DHT.AM2302, dbGPIO)
				elif (dbType == "DS18S20"):
					self.DS(dbId, W1ThermSensor.THERM_SENSOR_DS18S20, dbSerialNo)
				elif (dbType == "DS1822"):
					self.DS(dbId, W1ThermSensor.THERM_SENSOR_DS1822, dbSerialNo)
				elif (dbType == "DS18B20"):
					self.DS(dbId, W1ThermSensor.THERM_SENSOR_DS18B20, dbSerialNo)
				elif (dbType == "MAX31850K"):
					self.DS(dbId, W1ThermSensor.THERM_SENSOR_MAX31850K, dbSerialNo)
				else:
					self.log.warning('Server', 'Unknown sensor type for %s (%s)' % (dbName, dbType))
		except MySQLdb.Error, e:
			#Log exceptions
			try:
				self.log.error('API', 'MySQL Error [%d]: %s' % (e.args[0], e.args[1]))
	
			except IndexError:
				self.log.error('API', 'MySQL Error: %s' % str(e))
		finally:
			#Close database connection
			cursor.close()
			db.close()

	#---------------------------------------------------------------------------# 
	# SQL Query
	#---------------------------------------------------------------------------# 			
	def SQLQuery(self, sSQL):
		try:
			db = MySQLdb.connect(Config.DbHost, Config.DbUser, Config.DbPassword, Config.DbName)
			cursor = db.cursor()
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