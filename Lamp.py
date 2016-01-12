import datetime
import time
import MySQLdb
import pi_switch
import sys
import logging
from Sun import Sun
from Config import Config
from Log import Log

class Lamp:
	#---------------------------------------------------------------------------# 
	# Constructor
	#---------------------------------------------------------------------------# 
	def __init__(self):
		self.logger = logging.getLogger('cr-smart-home')
		self.log = Log()
		self.sun = Sun()
	
	#---------------------------------------------------------------------------# 
	# Send RF command
	#---------------------------------------------------------------------------# 
	def LampCmd(self, sCmd):
		# Warn if lamp command is empty
		if (len(sCmd) < 1):
			self.log.warning('Server', 'Lamp command is empty!')
			return 'Lamp command is empty!'

		# Send command
		sender = pi_switch.RCSwitchSender()
		sender.enableTransmit(Config.RPi_Pin_Transmitter)
		sender.sendDecimal(int(sCmd), 24)

		# Return
		return 'Done!'

	#---------------------------------------------------------------------------# 
	# Change status of lamp
	#---------------------------------------------------------------------------# 
	def LampPower(self, nId, sName, nPowerOn, sCmd):
		
		#Update database
		dbPowerOff = MySQLdb.connect(Config.DbHost, Config.DbUser, Config.DbPassword, Config.DbName)
		cursorPowerOff = dbPowerOff.cursor()
	
		sSQL = "UPDATE ha_lamp_objects SET LampPowerOn = %d, LampPowerOnMan = %d WHERE LampId = %d" % (nPowerOn, nPowerOn, nId)
	
		try:
			cursorPowerOff.execute(sSQL)
			dbPowerOff.commit()
		except MySQLdb.Error, e:
			dbPowerOff.rollback()
			self.log.error('Server', 'MySQL Error [%d]: %s' % (e.args[0], e.args[1]))
		except:
			self.log.error('Server', 'Unexpected error: %s' % (sys.exc_info()[0]))
		finally:
			dbPowerOff.close()
	
		#Log
		if (nPowerOn == 1):
			self.log.info('Server', 'Sending power on to %s (Cmd: %s)' % (sName, sCmd))
		else:
			self.log.info('Server', 'Sending power off to %s (Cmd: %s)' % (sName, sCmd))
	
		#Send command to Nexa Power Switch
		self.LampCmd(sCmd)
	
	
	#---------------------------------------------------------------------------# 
	# Schedule
	#---------------------------------------------------------------------------# 
	def Schedule(self):
		#DateTime
		dtNow = datetime.datetime.now()
		dtDateNow = datetime.datetime.now().date()
		nWeekdayNow = datetime.datetime.today().weekday()
		
		#Sun
		bSunIsDown = self.sun.sunIsDown();
		
		#Init variables
		dbId = 0
		dbName = ''
		dbPowerOn = 0
		dbCmdOn = ''
		dbCmdOff = ''
		dbWeekday = 0
		dbOn = ''
		dbOff = ''
		dbMode = 0
		nPowerOn = 0

		#Update database
		self.SQLQuery("Update ha_data SET DataText='OK', DataStatus=200, DataLastUpdated=NOW() WHERE DataName='Schedule'");
	
		#Connect to MySQL
		db = MySQLdb.connect(Config.DbHost, Config.DbUser, Config.DbPassword, Config.DbName)
		cursor = db.cursor()
	
		try:
			#Execure SQL-Query
			cursor.execute("CALL GetLampSchedulesSimple")
			results = cursor.fetchall()
		
			#Loop result from database
			for row in results:
				#Continue if object were started last loop
				if (dbId == row[0] and nPowerOn == 1):
					continue
				#Last object shouldn't be on
				elif (dbId > 0 and dbId <> row[0] and nPowerOn == 0 and dbPowerOn <> 0 and dbMode <> 0):
					self.LampPower(dbId, dbName, 0, dbCmdOff)
					
				#Move database row to variables
				dbId = row[0]
				dbName = row[1]
				dbPowerOn = row[2]
				dbCmdOn = row[3]
				dbCmdOff = row[4]
				dbWeekday = row[5]
				dbOn = row[6]
				dbOff = row[7]
				dbMode = row[8]
				
				#Calculate DateTime for start and stop
				if (nWeekdayNow == dbWeekday):
					sStart = '%s %s' % (dtDateNow, dbOn)
					sStop = '%s %s' % (dtDateNow, dbOff)
				else:
					sStart = '%s %s' % (dtDateNow - datetime.timedelta(days=1), dbOn)
					sStop = '%s %s' % (dtDateNow - datetime.timedelta(days=1), dbOff)
			
				#Convert string to datetime
				dtStart = datetime.datetime.strptime(sStart, '%Y-%m-%d %H:%M:%S')
				dtStop = datetime.datetime.strptime(sStop, '%Y-%m-%d %H:%M:%S')
			
				#Add extra day if stop date is over midnight
				if (dtStart > dtStop):
					dtStop += datetime.timedelta(days=1)
			
				#Start object
				if (dtNow > dtStart and dtNow < dtStop and (dbMode == 1 or (dbMode == 2 and bSunIsDown))):
					nPowerOn = 1
		
					if (dbPowerOn <> 1):
						self.LampPower(dbId, dbName, 1, dbCmdOn)
				else:
					nPowerOn = 0
				
			#Power off last object if not started
			if (dbId > 0 and nPowerOn == 0 and dbPowerOn <> 0 and dbMode <> 0):
				self.LampPower(dbId, dbName, 0, dbCmdOff)
	
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
	# Power to single lamp
	#---------------------------------------------------------------------------# 
	def PowerSingle(self, Id, PowerOn):
		# Connect to database
		db = MySQLdb.connect(Config.DbHost, Config.DbUser, Config.DbPassword, Config.DbName)
		cursor = db.cursor()
		
		# Select lamp from database
		try:
			cursor.execute("SELECT LampName, LampCmdOn, LampCmdOff FROM ha_lamp_objects WHERE LampId = %s" % Id)
			results = cursor.fetchone()
		
			#Move result to variables
			dbName = results[0]
			dbCmdOn = results[1]
			dbCmdOff = results[2]
		
			if (PowerOn == "1"):
				# Send power on command
				self.LampCmd(dbCmdOn)
				self.log.info('API', 'Sending power on to %s' % dbName)
			else:
				# Send power off command
				self.LampCmd(dbCmdOff)
				self.log.info('API', 'Sending power off to %s' % dbName)
		except MySQLdb.Error, e:
			# Log exceptions
			try:
				self.log.error('API', 'MySQL Error [%d]: %s' % (e.args[0], e.args[1]))
	
			except IndexError:
				self.log.error('API', 'MySQL Error: %s' % str(e))
			
		# Update database
		try:
			cursor.execute("UPDATE ha_lamp_objects SET LampPowerOnMan = %s WHERE LampId = %s" % (PowerOn, Id))
			db.commit()
		except MySQLdb.Error, e:
			db.rollback()
			self.log.error('API', 'MySQL Error [%d]: %s' % (e.args[0], e.args[1]))
		except:
			self.log.error('API', 'Unexpected error: %s' % (sys.exc_info()[0]))
		finally:
			# Close database connection
			cursor.close()
			db.close()
		
		return 'Done!'

	#---------------------------------------------------------------------------# 
	# Power to all lamps in room
	#---------------------------------------------------------------------------# 
	def PowerRoom(self, Id, PowerOn):
		# Connect to database
		db = MySQLdb.connect(Config.DbHost, Config.DbUser, Config.DbPassword, Config.DbName)
		cursor = db.cursor()
		
		try:
			# Select lamps from database
			cursor.execute("SELECT LampId, LampName, LampCmdOn, LampCmdOff, RoomName FROM ha_lamp_objects LEFT JOIN ha_rooms ON RoomId=LampRoomId WHERE LampRoomId = %s" % Id)
			results = cursor.fetchall()
		
			# Loop result from database
			for row in results:
				# Move result to variables
				dbId = row[0]
				dbName = row[1]
				dbCmdOn = row[2]
				dbCmdOff = row[3]
				dbRoomName = row[4]
			
				if (PowerOn == "1"):
					# Send power on command
					self.LampCmd(dbCmdOn)
				else:
					# Send power of command
					self.LampCmd(dbCmdOff)
			
			# Log
			if (PowerOn == "1"):
				self.log.info('API', 'Sending power on to room %s...' % dbRoomName)
			else:
				self.log.info('API', 'Sending power off to room %s...' % dbRoomName)
	
		except MySQLdb.Error, e:
			#Log exceptions
			try:
				self.log.error('API', 'MySQL Error [%d]: %s' % (e.args[0], e.args[1]))
	
			except IndexError:
				self.log.error('API', 'MySQL Error: %s' % str(e))
			
		#Update database
		try:
			cursor.execute("UPDATE ha_lamp_objects SET LampPowerOnMan = %s WHERE LampRoomId = %s" % (PowerOn, Id))
			db.commit()
		except MySQLdb.Error, e:
			db.rollback()
			self.log.error('API', 'MySQL Error [%d]: %s' % (e.args[0], e.args[1]))
		except:
			self.log.error('API', 'Unexpected error: %s' % (sys.exc_info()[0]))
		finally:
			#Close database connection
			cursor.close()
			db.close()
		
		return 'Done!'
		
	#---------------------------------------------------------------------------# 
	# Power to all lamps
	#---------------------------------------------------------------------------# 
	def PowerAll(self, PowerOn):
		# Connect to database
		db = MySQLdb.connect(Config.DbHost, Config.DbUser, Config.DbPassword, Config.DbName)
		cursor = db.cursor()
		
		try:
			# Select lamps from database
			cursor.execute("SELECT LampCmdOn, LampCmdOff FROM ha_lamp_objects WHERE LampIncInAll = 1")
			results = cursor.fetchall()
		
			# Loop result from database
			for row in results:
				# Move result to variables
				dbCmdOn = row[0]
				dbCmdOff = row[1]
			
				if (PowerOn == "1"):
					# Send power on command
					self.LampCmd(dbCmdOn)
				else:
					# Send power on command
					self.LampCmd(dbCmdOff)
			
			# Log
			if (PowerOn == "1"):
				self.log.info('API', 'Sending power on to all lamps')
			else:
				self.log.info('API', 'Sending power off to all lamps')
	
		except MySQLdb.Error, e:
			#Log exceptions
			try:
				self.log.error('API', 'MySQL Error [%d]: %s' % (e.args[0], e.args[1]))
	
			except IndexError:
				self.log.error('API', 'MySQL Error: %s' % str(e))
			
		#Update database
		try:
			cursor.execute("UPDATE ha_lamp_objects SET LampPowerOnMan = %s WHERE LampIncInAll = 1" % PowerOn)
			db.commit()
		except MySQLdb.Error, e:
			db.rollback()
			self.log.error('API', 'MySQL Error [%d]: %s' % (e.args[0], e.args[1]))
		except:
			self.log.error('API', 'Unexpected error: %s' % (sys.exc_info()[0]))
		finally:
			#Close database connection
			cursor.close()
			db.close()
		
		return 'Done!'
		
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