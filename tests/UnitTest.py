import unittest
import datetime
import Adafruit_DHT
import json
import hashlib
from base64 import b64encode
import sys
sys.path.append("..")
from API import app
from Log import Log
from Sun import Sun
from Lamp import Lamp
from Sensor import Sensor
from Upgrade import Upgrade
from Weather import Weather
from w1thermsensor import W1ThermSensor, NoSensorFoundError, SensorNotReadyError, UnsupportedUnitError

class CrSmartHomeTestCase(unittest.TestCase):

	API_Username = 'admin'
	API_Password = ''
	API_UserAgent = 'CR Smart Home Test'
	
	def create_app(self):
		app = Flask(__name__)
		app.config['TESTING'] = True
		return app 

	def setUp(self):
		# API Login
		data = json.dumps({
			'username': self.API_Username,
			'password': hashlib.sha512('admin123').hexdigest()
		})

		tester = app.test_client(self)
		response = tester.post('/ha/api/v1.0/login', data=data, follow_redirects=True, content_type='application/json', environ_base={'HTTP_USER_AGENT': self.API_UserAgent})
		self.assertEqual(response.status_code, 200)
		self.API_Password = hashlib.sha512("%s%s" % (json.loads(response.data)["login"]["password"], self.API_UserAgent)).hexdigest()
		#self.assertEqual("%s" % self.API_Password, {"result": 8})

	def test_API_get_lamps(self):
		# API
		headers = {
			'Authorization': 'Basic ' + b64encode("{0}:{1}".format(self.API_Username, self.API_Password))
		}

		tester = app.test_client(self)
		response = tester.get('/ha/api/v1.0/lamps', follow_redirects=True, headers=headers, environ_base={'HTTP_USER_AGENT': self.API_UserAgent})
		self.assertEqual(response.status_code, 200)
		#self.assertEqual(json.loads(response.data), {"result": 8})
		
	def test_API_get_lamp(self):
		# API
		headers = {
			'Authorization': 'Basic ' + b64encode("{0}:{1}".format(self.API_Username, self.API_Password))
		}

		tester = app.test_client(self)
		response = tester.get('/ha/api/v1.0/lamps/2', follow_redirects=True, headers=headers, environ_base={'HTTP_USER_AGENT': self.API_UserAgent})
		self.assertEqual(response.status_code, 200)
		#self.assertEqual(json.loads(response.data), {"result": 8})
		
	def test_API_power_single(self):
		# API
		headers = {
			'Authorization': 'Basic ' + b64encode("{0}:{1}".format(self.API_Username, self.API_Password))
		}
		
		data = json.dumps({
			'id': "2",
			'PowerOn': "0"
		})

		tester = app.test_client(self)
		response = tester.post('/ha/api/v1.0/lamps/single', data=data, follow_redirects=True, headers=headers, content_type='application/json', environ_base={'HTTP_USER_AGENT': self.API_UserAgent})
		self.assertEqual(response.status_code, 200)		
		#self.assertEqual("%s" % self.API_Password, {"result": 8})
		
		data = json.dumps({
			'id': "2",
			'PowerOn': "1"
		})

		response = tester.post('/ha/api/v1.0/lamps/single', data=data, follow_redirects=True, headers=headers, content_type='application/json', environ_base={'HTTP_USER_AGENT': self.API_UserAgent})
		self.assertEqual(response.status_code, 200)		
		#self.assertEqual("%s" % self.API_Password, {"result": 8})
		
	def test_API_power_room(self):
		# API
		headers = {
			'Authorization': 'Basic ' + b64encode("{0}:{1}".format(self.API_Username, self.API_Password))
		}
		
		data = json.dumps({
			'id': "1",
			'PowerOn': "0"
		})

		tester = app.test_client(self)
		response = tester.post('/ha/api/v1.0/lamps/room', data=data, follow_redirects=True, headers=headers, content_type='application/json', environ_base={'HTTP_USER_AGENT': self.API_UserAgent})
		self.assertEqual(response.status_code, 200)		
		#self.assertEqual("%s" % self.API_Password, {"result": 8})
		
		data = json.dumps({
			'id': "1",
			'PowerOn': "1"
		})

		response = tester.post('/ha/api/v1.0/lamps/room', data=data, follow_redirects=True, headers=headers, content_type='application/json', environ_base={'HTTP_USER_AGENT': self.API_UserAgent})
		self.assertEqual(response.status_code, 200)		
		#self.assertEqual("%s" % self.API_Password, {"result": 8})
		
	def test_API_power_all(self):
		# API
		headers = {
			'Authorization': 'Basic ' + b64encode("{0}:{1}".format(self.API_Username, self.API_Password))
		}
		
		data = json.dumps({
			'PowerOn': "0"
		})

		tester = app.test_client(self)
		response = tester.post('/ha/api/v1.0/lamps/all', data=data, follow_redirects=True, headers=headers, content_type='application/json', environ_base={'HTTP_USER_AGENT': self.API_UserAgent})
		self.assertEqual(response.status_code, 200)		
		#self.assertEqual("%s" % self.API_Password, {"result": 8})
		
		data = json.dumps({
			'PowerOn': "1"
		})

		response = tester.post('/ha/api/v1.0/lamps/all', data=data, follow_redirects=True, headers=headers, content_type='application/json', environ_base={'HTTP_USER_AGENT': self.API_UserAgent})
		self.assertEqual(response.status_code, 200)		
		#self.assertEqual("%s" % self.API_Password, {"result": 8})
		
	def test_API_dashboard(self):
		# API
		headers = {
			'Authorization': 'Basic ' + b64encode("{0}:{1}".format(self.API_Username, self.API_Password))
		}

		tester = app.test_client(self)
		response = tester.get('/ha/api/v1.0/dashboard', follow_redirects=True, headers=headers, environ_base={'HTTP_USER_AGENT': self.API_UserAgent})
		self.assertEqual(response.status_code, 200)
		#self.assertEqual(json.loads(response.data), {"result": 8})

	def test_Lamp(self):
		# Lamp
		lamp = Lamp()
		assert lamp.LampCmd("1234") == 'Done!'
		lamp.LampPower(10, "Test", 1, "1234")
		lamp.LampPower(10, "Test", 0, "1234")
		assert lamp.PowerSingle(10, "1") == 'Done!'
		assert lamp.PowerSingle(10, "0") == 'Done!'
		assert lamp.PowerRoom(1, "1") == 'Done!'
		assert lamp.PowerRoom(1, "0") == 'Done!'
		assert lamp.PowerAll("1") == 'Done!'
		assert lamp.PowerAll("0") == 'Done!'
		lamp.Schedule()
		lamp.SQLQuery("INSERT INTO ha_data (DataId, DataName, DataText, DataStatus, DataLastUpdated) VALUES (9999, 'Test', 'Test', 200, NOW()) ON DUPLICATE KEY UPDATE DataText = VALUES(DataText), DataStatus = VALUES(DataStatus), DataLastUpdated = VALUES(DataLastUpdated)")

	def test_Log(self):
		# Log
		log = Log()
		log.debug("Test", "Debug")
		log.info("Test", "Info")
		log.warning("Test", "Warning")
		log.error("Test", "Error")
		log.SQLQuery("INSERT INTO ha_data (DataId, DataName, DataText, DataStatus, DataLastUpdated) VALUES (9999, 'Test', 'Test', 200, NOW()) ON DUPLICATE KEY UPDATE DataText = VALUES(DataText), DataStatus = VALUES(DataStatus), DataLastUpdated = VALUES(DataLastUpdated)")

	def test_Sensor(self):
		sensor = Sensor()
		sensor.DHT(1, Adafruit_DHT.DHT22, 9)
		sensor.DS(2, W1ThermSensor.THERM_SENSOR_DS18B20, "0000072f3122")
		sensor.readAll()
		sensor.SQLQuery("INSERT INTO ha_data (DataId, DataName, DataText, DataStatus, DataLastUpdated) VALUES (9999, 'Test', 'Test', 200, NOW()) ON DUPLICATE KEY UPDATE DataText = VALUES(DataText), DataStatus = VALUES(DataStatus), DataLastUpdated = VALUES(DataLastUpdated)")

	def test_Sun(self):
		sun = Sun()
		now = datetime.datetime.now()

		sun.sunIsDown()
		sun.sunIsUp()
		sun.UpdateDb()
		assert sun.adjustAngle(-180) == 180
		assert sun.adjustAngle(540) == 180
		assert sun.adjustTime(-12) == 12
		assert sun.adjustTime(36) == 12
		sun.sunrise(now, 57.7007, 11.9682)
		sun.sunset(now, 57.7007, 11.9682)
		sun.SQLQuery("INSERT INTO ha_data (DataId, DataName, DataText, DataStatus, DataLastUpdated) VALUES (9999, 'Test', 'Test', 200, NOW()) ON DUPLICATE KEY UPDATE DataText = VALUES(DataText), DataStatus = VALUES(DataStatus), DataLastUpdated = VALUES(DataLastUpdated)")

	def test_Upgrade(self):
		# Upgrade
		upgrade = Upgrade()
		upgrade.GetCurrentVersion()
		assert upgrade.VersionToInt('v1.0.6') == [1, 0, 6]
		upgrade.Upgrade()
		upgrade.SQLQuery("INSERT INTO ha_data (DataId, DataName, DataText, DataStatus, DataLastUpdated) VALUES (9999, 'Test', 'Test', 200, NOW()) ON DUPLICATE KEY UPDATE DataText = VALUES(DataText), DataStatus = VALUES(DataStatus), DataLastUpdated = VALUES(DataLastUpdated)")

	def test_Weather(self):
		# Weather
		weather = Weather()
		weather.UpdateCurrentWeather()
		weather.GetSettings()
		weather.SQLQuery("INSERT INTO ha_data (DataId, DataName, DataText, DataStatus, DataLastUpdated) VALUES (9999, 'Test', 'Test', 200, NOW()) ON DUPLICATE KEY UPDATE DataText = VALUES(DataText), DataStatus = VALUES(DataStatus), DataLastUpdated = VALUES(DataLastUpdated)")

if __name__ == '__main__':
	unittest.main()