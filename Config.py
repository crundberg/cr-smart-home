import logging

class Config:
	#---------------------------------------------------------------------------# 
	# General settings
	#---------------------------------------------------------------------------# 
	Version = 'v0.1.7'

	#---------------------------------------------------------------------------# 
	# GPIO Pins on Raspberry Pi
	#---------------------------------------------------------------------------#
	RPi_Pin_Transmitter = 0	# Use WiringPi pin 0
	RPi_Pin_Receiver = 2	# Use WiringPi pin 2
	
	#---------------------------------------------------------------------------# 
	# Logging
	#---------------------------------------------------------------------------# 
	Log_Filename = '/home/pi/Documents/cr-smart-home-webgui/logs/main.log' # Path to logfile
	Log_Level = logging.INFO        # Log level to save

	#---------------------------------------------------------------------------# 
	# Database settings
	#---------------------------------------------------------------------------# 
	DbHost = "localhost"			# Hostname
	DbUser = "hauser"				# Username
	DbPassword = "homeautomation"	# Password
	DbName = "crsmarthome"			# Database name