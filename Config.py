import logging

class Config:
	#---------------------------------------------------------------------------# 
	# General settings
	#---------------------------------------------------------------------------# 
	Version = 'v0.1'
	City = 'Goteborg'
	Latitude = 57.70887	#Latitude for Goteborg
	Longitude = 11.97456	#Longitude for Goteborg

	#---------------------------------------------------------------------------# 
	# GPIO Pins on Raspberry Pi
	#---------------------------------------------------------------------------#
	RPi_Pin_Transmitter = 0	# Use WiringPi pin 0
	RPi_Pin_Receiver = 2	# Use WiringPi pin 2

	#---------------------------------------------------------------------------# 
	# Logging
	#---------------------------------------------------------------------------# 
	Log_Filename = '/var/www/html/ha/logs/main.log'
	Log_Level = logging.INFO

	#---------------------------------------------------------------------------# 
	# Database settings
	#---------------------------------------------------------------------------# 
	DbHost = "localhost"
	DbUser = "hauser"
	DbPassword = "homeautomation"
	DbName = "homeautomation"