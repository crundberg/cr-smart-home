import MySQLdb
import collections
import sys
from flask import Flask, jsonify, abort, make_response, request
from flask.ext.httpauth import HTTPBasicAuth
from Lamp import Lamp
from Config import Config

app = Flask(__name__)
auth = HTTPBasicAuth()

#---------------------------------------------------------------------------# 
# Hello World
#---------------------------------------------------------------------------#
@app.route("/")
@auth.login_required
def hello():
	return "Hello World!"

#---------------------------------------------------------------------------# 
# Get all lamps
#---------------------------------------------------------------------------#
@app.route("/ha/api/v1.0/lamps", methods=['GET'])
@auth.login_required
def get_lamps():
	lamps = []

	#Connect to MySQL
	db = MySQLdb.connect(Config.DbHost, Config.DbUser, Config.DbPassword, Config.DbName)
	cursor = db.cursor()

	try:
		#Execure SQL-Query
		cursor.execute("SELECT * FROM ha_lamp_objects")
		results = cursor.fetchall()
	
		#Loop result from database
		for row in results:
			#Move database row to variables
			d = collections.OrderedDict()
			d['Id'] = row[0]
			d['Name'] = row[1]
			d['IO'] = row[2]
			d['Type'] = row[3]
			d['PowerOn'] = row[4]
			d['PowerOnMan'] = row[5]
			d['CmdOn'] = row[6]
			d['CmdOff'] = row[7]
			lamps.append(d)
	except MySQLdb.Error, e:
		#Log exceptions
		try:
			return make_response(jsonify({'MySQL-Error': e.args[1]}), 404)
		except IndexError:
			return make_response(jsonify({'MySQL-Error': str(e)}), 404)

	finally:
		#Close database connection
		cursor.close()
		db.close()

	return jsonify({'lamps': lamps})

#---------------------------------------------------------------------------# 
# Get one lamp
#---------------------------------------------------------------------------#
@app.route('/ha/api/v1.0/lamps/<int:lamp_id>', methods=['GET'])
@auth.login_required
def get_lamp(lamp_id):
	#Connect to MySQL
	db = MySQLdb.connect(Config.DbHost, Config.DbUser, Config.DbPassword, Config.DbName)
	cursor = db.cursor()

	try:
		#Execure SQL-Query
		cursor.execute("SELECT * FROM ha_lamp_objects WHERE LampId=%d" % lamp_id)
		results = cursor.fetchall()
	
		#Loop result from database
		for row in results:
			#Move database row to variables
			d = collections.OrderedDict()
			d['Id'] = row[0]
			d['Name'] = row[1]
			d['IO'] = row[2]
			d['Type'] = row[3]
			d['PowerOn'] = row[4]
			d['PowerOnMan'] = row[5]
			d['CmdOn'] = row[6]
			d['CmdOff'] = row[7]
	except MySQLdb.Error, e:
		#Log exceptions
		try:
			return make_response(jsonify({'MySQL-Error': e.args[1]}), 404)
		except IndexError:
			return make_response(jsonify({'MySQL-Error': str(e)}), 404)

	finally:
		#Close database connection
		cursor.close()
		db.close()

	return jsonify({'lamps': d})

#---------------------------------------------------------------------------# 
# Send RF command to lamp
#---------------------------------------------------------------------------#
@app.route('/ha/api/v1.0/lamps', methods=['POST'])
@auth.login_required
def power_lamp():
	if not request.json or not 'id' in request.json:
		abort(400)

	lamp = Lamp()
	result = lamp.LampCmd(request.json.get('cmd', ""))

	json = {
		'id': request.json['id'],
		'cmd': request.json.get('cmd', ""),
		'result': result
	}

	return jsonify({'lamp': json})

#---------------------------------------------------------------------------# 
# Send power on to all lamps
#---------------------------------------------------------------------------#
@app.route('/ha/api/v1.0/lamps/allon', methods=['POST'])
@auth.login_required
def powerallon():
	lamp = Lamp()
	result = lamp.PowerOnAllObjects()

	json = {
		'result': result
	}

	return jsonify({'lamp': json})
	
#---------------------------------------------------------------------------# 
# Send power off to all lamps
#---------------------------------------------------------------------------#
@app.route('/ha/api/v1.0/lamps/alloff', methods=['POST'])
@auth.login_required
def poweralloff():
	lamp = Lamp()
	result = lamp.PowerOffAllObjects()

	json = {
		'result': result
	}

	return jsonify({'lamp': json})

#---------------------------------------------------------------------------# 
# Authenticate
#---------------------------------------------------------------------------#
@auth.verify_password
def verify_password(username, password):
	db = MySQLdb.connect(Config.DbHost, Config.DbUser, Config.DbPassword, Config.DbName)
	
	pwd = password.split(";;;")
	
	cursor = db.cursor()
	cursor.execute("SELECT * FROM ha_users WHERE UserName = '" + username + "' AND SHA2(CONCAT(UserPassword, '" + pwd[1] + "'), 512) = '" + pwd[0] + "'")
	data = cursor.fetchone()
    
	if data is None:
		return False
	else:
		return True

#---------------------------------------------------------------------------# 
# 404 Error
#---------------------------------------------------------------------------#
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

#---------------------------------------------------------------------------# 
# Start app
#---------------------------------------------------------------------------#
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=False)
