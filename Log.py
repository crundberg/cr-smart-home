import logging
import MySQLdb
import sys
from Config import Config

class Log:
	#---------------------------------------------------------------------------# 
	# Constructor
	#---------------------------------------------------------------------------# 
	def __init__(self):
		self.logger = logging.getLogger('cr-smart-home')

	#---------------------------------------------------------------------------# 
	# Debug
	#---------------------------------------------------------------------------# 
	def debug(self, Name, Message):
		self.SQLQuery("INSERT INTO ha_log (LogDate, LogName, LogLevel, LogMessage) VALUES (NOW(), '%s', 'Debug', '%s')" % (Name, Message))
	
	#---------------------------------------------------------------------------# 
	# Info
	#---------------------------------------------------------------------------# 
	def info(self, Name, Message):
		self.SQLQuery("INSERT INTO ha_log (LogDate, LogName, LogLevel, LogMessage) VALUES (NOW(), '%s', 'Info', '%s')" % (Name, Message))
		
	#---------------------------------------------------------------------------# 
	# Warning
	#---------------------------------------------------------------------------# 
	def warning(self, Name, Message):
		self.SQLQuery("INSERT INTO ha_log (LogDate, LogName, LogLevel, LogMessage) VALUES (NOW(), '%s', 'Warning', '%s')" % (Name, Message))
		
	#---------------------------------------------------------------------------# 
	# Error
	#---------------------------------------------------------------------------# 
	def error(self, Name, Message):
		self.SQLQuery("INSERT INTO ha_log (LogDate, LogName, LogLevel, LogMessage) VALUES (NOW(), '%s', 'Error', '%s')" % (Name, Message))

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
			self.logger.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
		except:
			self.logger.error("Unexpected error: %s" % (sys.exc_info()[0]))
		finally:
			cursor.close()
			db.close()