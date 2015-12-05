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
	RPi_Pin_Transmitter = 2	# Use WiringPi pin 2
	RPi_Pin_Emitter = 0	# Use WiringPi pin 0

	#---------------------------------------------------------------------------# 
	# Database settings
	#---------------------------------------------------------------------------# 
	DbHost = "localhost"
	DbUser = "hauser"
	DbPassword = "homeautomation"
	DbName = "homeautomation"