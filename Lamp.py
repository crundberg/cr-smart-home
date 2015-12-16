import datetime
import time
import MySQLdb
import pi_switch
import logging
import sys
from Config import Config

logger = logging.getLogger('home-automation')

class Lamp:
	#---------------------------------------------------------------------------# 
	# Constructor
	#---------------------------------------------------------------------------# 
	def __init__(self):
		self.nHeartbeat = 0

	#---------------------------------------------------------------------------# 
	# Send RF command
	#---------------------------------------------------------------------------# 
	def LampCmd(self, sCmd):
		if (len(sCmd) < 1):
			logger.warning('Lamp command is empty!')
			return 'Lamp command is empty!'
	
		# Send command
                for x in range(0, Config.RF_Command_Repeat):
                        sender = pi_switch.RCSwitchSender()
                        sender.enableTransmit(Config.RPi_Pin_Transmitter)
                        sender.sendDecimal(int(sCmd), 24)
                        
                        time.sleep(Config.RF_Command_Delay)
	
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
			logger.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
		except:
			logger.error("Unexpected error: %s" % (sys.exc_info()[0]))
		finally:
			dbPowerOff.close()
	
		#Log
		if (nPowerOn == 1):
			logger.info("Sending power on to %s (Cmd: '%s')" % (sName, sCmd))
		else:
			logger.info("Sending power off to %s (Cmd: '%s')" % (sName, sCmd))
	
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
		
		#Init variables
		dbId = 0
		dbName = ''
		dbIO = ''
		dbPowerOn = 0
		dbCmdOn = ''
		dbCmdOff = ''
		dbWeekday = 0
		dbOn = ''
		dbOff = ''
		dbMode = 0
		nPowerOn = 0

		#Log heartbeat
		if (Config.Log_Heartbeat > 0):
                        self.nHeartbeat += 1

		if (self.nHeartbeat >= Config.Log_Heartbeat):
			self.nHeartbeat = 0
			logger.info('Heartbeat')
	
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
				elif (dbId > 0 and dbId <> row[0] and nPowerOn == 0 and dbPowerOn <> 0):
					self.LampPower(dbId, dbName, 0, dbCmdOff)
					
				#Move database row to variables
				dbId = row[0]
				dbName = row[1]
				dbIO = row[2]
				dbPowerOn = row[3]
				dbCmdOn = row[4]
				dbCmdOff = row[5]
				dbWeekday = row[6]
				dbOn = row[7]
				dbOff = row[8]
				dbMode = row[9]
				
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
				if (dtNow > dtStart and dtNow < dtStop):
					nPowerOn = 1
	
					if (dbPowerOn <> 1):
						self.LampPower(dbId, dbName, 1, dbCmdOn)
				else:
					nPowerOn = 0
				
			#Power off last object if not started
			if (dbId > 0 and nPowerOn == 0 and dbPowerOn <> 0):
				self.LampPower(dbId, dbName, 0, dbCmdOff)
	
		except MySQLdb.Error, e:
			#Log exceptions
			try:
				logger.Error('MySQL Error [%d]: %s' % (e.args[0], e.args[1]))
	
			except IndexError:
				logger.Error('MySQL Error: %s' % str(e))
		finally:
			#Close database connection
			cursor.close()
			db.close()
