import datetime
import time
import MySQLdb
import pi_switch
import sys
from Sun import Sun
from Config import Config
from Log import Log

class Lamp:
	#---------------------------------------------------------------------------# 
	# Constructor
	#---------------------------------------------------------------------------# 
	def __init__(self):
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
	# Loop all lamp objects
	#---------------------------------------------------------------------------# 
	def LoopLampObjects(self):
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
	# Power on all lamp objects
	#---------------------------------------------------------------------------# 
	def PowerRoom(self, Id, PowerOn):
		#Loop lamps och power on
		dbPowerRoom = MySQLdb.connect(Config.DbHost, Config.DbUser, Config.DbPassword, Config.DbName)
		cursorPowerRoom = dbPowerRoom.cursor()
		
		try:
			#Execure SQL-Query
			cursorPowerRoom.execute("SELECT LampId, LampName, LampCmdOn, LampCmdOff, RoomName FROM ha_lamp_objects LEFT JOIN ha_rooms ON RoomId=LampRoomId WHERE LampRoomId = %s" % Id)
			results = cursorPowerRoom.fetchall()
		
			#Loop result from database
			for row in results:
				#Move database row to variables
				dbId = row[0]
				dbName = row[1]
				dbCmdOn = row[2]
				dbCmdOff = row[3]
				dbRoomName = row[4]
			
				if (PowerOn == "1"):
					self.LampCmd(dbCmdOn)
				else:
					self.LampCmd(dbCmdOff)
			
			if (PowerOn == "1"):
				self.log.info('Server', 'Sending power on to room %s...' % dbRoomName)
			else:
				self.log.info('Server', 'Sending power off to room %s...' % dbRoomName)
	
		except MySQLdb.Error, e:
			#Log exceptions
			try:
				self.log.error('Server', 'MySQL Error [%d]: %s' % (e.args[0], e.args[1]))
	
			except IndexError:
				self.log.error('Server', 'MySQL Error: %s' % str(e))
		finally:
			#Close database connection
			cursorPowerRoom.close()
			dbPowerRoom.close()
			
		#Update database
		try:
			cursorPowerRoom.execute("UPDATE ha_lamp_objects SET LampPowerOnMan = %s WHERE LampRoomId = %s" % (PowerIn, Id))
			dbPowerRoom.commit()
		except MySQLdb.Error, e:
			dbPowerRoom.rollback()
			self.log.error('Server', 'MySQL Error [%d]: %s' % (e.args[0], e.args[1]))
		except:
			self.log.error('Server', 'Unexpected error: %s' % (sys.exc_info()[0]))
		
		return 'Done!'

	#---------------------------------------------------------------------------# 
	# Power on all lamp objects
	#---------------------------------------------------------------------------# 
	def PowerOnAllObjects(self):
		self.log.info('Server', 'Sending power on to all objects..')

		#Update database
		dbPowerAllOn = MySQLdb.connect(Config.DbHost, Config.DbUser, Config.DbPassword, Config.DbName)
		cursorPowerAllOn = dbPowerAllOn.cursor()

		try:
			cursorPowerAllOn.execute("UPDATE ha_lamp_objects SET LampPowerOnMan = 1 WHERE LampIncInAll = 1")
			dbPowerAllOn.commit()
		except MySQLdb.Error, e:
			dbPowerAllOn.rollback()
			self.log.error('Server', 'MySQL Error [%d]: %s' % (e.args[0], e.args[1]))
		except:
			self.log.error('Server', 'Unexpected error: %s' % (sys.exc_info()[0]))

		#Loop lamps och power on
		try:
			#Execure SQL-Query
			cursorPowerAllOn.execute("SELECT LampId, LampName, LampCmdOn FROM ha_lamp_objects WHERE LampIncInAll = 1")
			results = cursorPowerAllOn.fetchall()
		
			#Loop result from database
			for row in results:
				#Move database row to variables
				dbId = row[0]
				dbName = row[1]
				dbCmdOn = row[2]
				
				self.LampCmd(dbCmdOn)
	
		except MySQLdb.Error, e:
			#Log exceptions
			try:
				self.log.error('Server', 'MySQL Error [%d]: %s' % (e.args[0], e.args[1]))
	
			except IndexError:
				self.log.error('Server', 'MySQL Error: %s' % str(e))
		finally:
			#Close database connection
			cursorPowerAllOn.close()
			dbPowerAllOn.close()
		
		return 'Done!'

	#---------------------------------------------------------------------------# 
	# Power off all lamp objects
	#---------------------------------------------------------------------------# 
	def PowerOffAllObjects(self):
		self.log.info('Server', 'Sending power off to all objects..')

		#Update database
		dbPowerAllOff = MySQLdb.connect(Config.DbHost, Config.DbUser, Config.DbPassword, Config.DbName)
		cursorPowerAllOff = dbPowerAllOff.cursor()

		try:
			cursorPowerAllOff.execute("UPDATE ha_lamp_objects SET LampPowerOnMan = 0 WHERE LampIncInAll = 1")
			dbPowerAllOff.commit()
		except MySQLdb.Error, e:
			dbPowerAllOff.rollback()
			self.log.error('Server', 'MySQL Error [%d]: %s' % (e.args[0], e.args[1]))
		except:
			self.log.error('Server', 'Unexpected error: %s' % (sys.exc_info()[0]))

		#Loop lamps och power off
		try:
			#Execure SQL-Query
			cursorPowerAllOff.execute("SELECT LampId, LampName, LampCmdOff FROM ha_lamp_objects WHERE LampIncInAll = 1")
			results = cursorPowerAllOff.fetchall()
		
			#Loop result from database
			for row in results:
				#Move database row to variables
				dbId = row[0]
				dbName = row[1]
				dbCmdOff = row[2]
				
				self.LampCmd(dbCmdOff)
	
		except MySQLdb.Error, e:
			#Log exceptions
			try:
				self.log.error('Server', 'MySQL Error [%d]: %s' % (e.args[0], e.args[1]))
	
			except IndexError:
				self.log.error('Server', 'MySQL Error: %s' % str(e))
		finally:
			#Close database connection
			cursorPowerAllOff.close()
			dbPowerAllOff.close()
		
		return 'Done!'
		
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