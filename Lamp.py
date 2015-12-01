import datetime
import time
import MySQLdb

def LampPowerOn(nId, sName, nPowerOn):
	#Lamp power is already on
	if (nPowerOn == 1):
		return;

	#TODO: Send command to Nexa Power Switch


	#Update database
	dbPowerOn = MySQLdb.connect("localhost", "hauser", "homeautomation", "homeautomation")
	cursorPowerOn = dbPowerOn.cursor()

	sSQL = "UPDATE ha_lamp_objects SET LampPowerOn = 1 WHERE LampId = %d" % nId

	try:
		cursorPowerOn.execute(sSQL)
		dbPowerOn.commit()
	except:
		dbPowerOn.rollback()
	finally:
		cursorPowerOn.close()
		dbPowerOn.close()

	#Log
	print '%s: Sending power on to %s' % (datetime.datetime.now(), sName)
	return;

def LampPowerOff(nId, sName, nPowerOn):
	#Lamp power is already off
	if (nPowerOn == 0):
		return;

	#TODO: Send command to Nexa Power Switch


	#Update database
	dbPowerOff = MySQLdb.connect("localhost", "hauser", "homeautomation", "homeautomation")
	cursorPowerOff = dbPowerOff.cursor()

	sSQL = "UPDATE ha_lamp_objects SET LampPowerOn = 0 WHERE LampId = %d" % nId

	try:
		cursorPowerOff.execute(sSQL)
		dbPowerOff.commit()
	except:
		dbPowerOff.rollback()
	finally:
		dbPowerOff.close()

	#Log
	print "%s: Sending power off to %s" % (datetime.datetime.now(), sName)
	return;

def LoopLampObjects():
	#DateTime
	dtNow = datetime.datetime.now()
	dtDateNow = datetime.datetime.now().date()
	nWeekdayNow = datetime.datetime.today().weekday()
	
	#Init variables
	dbId = 0
	dbName = ''
	dbIO = ''
	dbPowerOn = 0
	dbWeekday = 0
	dbOn = ''
	dbOff = ''
	dbMode = 0
	nPowerOn = 0

	#Connect to MySQL
	db = MySQLdb.connect("localhost", "hauser", "homeautomation", "homeautomation")
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
			elif (dbId > 0 and dbId <> row[0] and nPowerOn == 0):
				LampPowerOff(dbId, dbName, dbPowerOn)
				
			#Move database row to variables
			dbId = row[0]
			dbName = row[1]
			dbIO = row[2]
			dbPowerOn = row[3]
			dbWeekday = row[4]
			dbOn = row[5]
			dbOff = row[6]
			dbMode = row[7]
			
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
				LampPowerOn(dbId, dbName, dbPowerOn)
			else:
				nPowerOn = 0
			
			#Log
			#print '%s: %s (%s), Weekday: %s, Start: %s, Stop: %s, Active: %s, PowerOn: %d' % (dbId, dbName, dbIO, dbWeekday, dtStart, dtStop, dbMode, dbPowerOn)
		
		#Power off last object if not started
		if (dbId > 0 and nPowerOn == 0):
			LampPowerOff(dbId, dbName, dbPowerOn)
	except MySQLdb.Error, e:
		#Log exceptions
		try:
			print 'MySQL Error [%d]: %s' % (e.args[0], e.args[1])
		except IndexError:
			print 'MySQL Error: %s' % str(e)
	finally:
		#Close database connection
		cursor.close()
		db.close()

	return;