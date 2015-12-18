import logging

class Config:
	#---------------------------------------------------------------------------# 
	# General settings
	#---------------------------------------------------------------------------# 
	Version = 'v0.1'
	City = 'Goteborg'
	Latitude = 57.70887		#Latitude for Goteborg
	Longitude = 11.97456	#Longitude for Goteborg

	#---------------------------------------------------------------------------# 
	# GPIO Pins on Raspberry Pi
	#---------------------------------------------------------------------------#
	RPi_Pin_Transmitter = 0	# Use WiringPi pin 0
	RPi_Pin_Receiver = 2	# Use WiringPi pin 2

	#---------------------------------------------------------------------------# 
	# Logging
	#---------------------------------------------------------------------------# 
	Log_Filename = '/home/pi/Documents/home-automation-webgui/logs/main.log' # Path to logfile
	Log_Level = logging.INFO        # Log level to save
	Log_Heartbeat = 60              # Log heartbeat every x minut (0=Disable)

	#---------------------------------------------------------------------------# 
	# Database settings
	#---------------------------------------------------------------------------# 
	DbHost = "localhost"            # Hostname
	DbUser = "hauser"               # Username
	DbPassword = "homeautomation"   # Password
	DbName = "homeautomation"       # Database name

	#---------------------------------------------------------------------------# 
	# RF command settings
	#---------------------------------------------------------------------------#
	RF_Command_Repeat = 3	# Number of times to repeat command
	RF_Command_Delay = 0	# Time in seconds between the repeats

	#---------------------------------------------------------------------------# 
	# Sun settings
	#---------------------------------------------------------------------------# 
	Zenith = 90.83333	# Sun's zenith for sunrise/sunset
	LocalOffset = 1		# Offset from UTC (GMT)