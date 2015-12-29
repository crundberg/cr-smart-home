import logging
import MySQLdb
import sys
from Config import Config

logger = logging.getLogger('home-automation')

class Log:
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
			db = MySQLdb.connect(Config.DbHost, Config.DbUser, Config.DbPassword, Config.DbName)
			cursor = db.cursor()
		
			try:
				cursor.execute(sSQL)
				db.commit()
			except MySQLdb.Error, e:
				db.rollback()
				logger.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
			except:
				logger.error("Unexpected error: %s" % (sys.exc_info()[0]))
			finally:
				cursor.close()
				db.close()