class Lamp:

	LampCount = 0

	def __init__(self, Name, IO, TimeStart, TimeStop, Active):
		self.Name = Name
		self.IO = IO
		self.TimeStart = TimeStart
		self.TimeStop = TimeStop
		self.Active = Active
		self.Started = 0
		Lamp.LampCount += 1

	def displayCount(self):
		print "Total Lamps %d" % Lamp.LampCount

	def displayLamp(self):
		print "Name: %s, Start time: %s, Stop time: %s" % (self.Name, self.TimeStart, self.TimeStop)
