var sensorDHT = require('node-dht-sensor');
var sensorDS = require('ds18b20');
var sensorTSL = require('sensor_tsl2561');
var mysql = require('./../mysql.js');
var config = require('./../config.json');

//---------------------------------------------------------------------------
// DHT
//---------------------------------------------------------------------------
function DHT(Id, Type, GPIO) {
	sensorDHT.read(Type, GPIO, function(err, temperature, humidity) {
		if (err) {
			console.log(err);
			return;
		}
			
		// Update database
		mysql.getConnection(function(err, connection) {
			connection.query("INSERT INTO cr_sensors_log (LogSensorId, LogDate, LogValue1, LogValue2) VALUES (?, NOW(), ?, ?)", [Id, temperature.toFixed(1), humidity.toFixed(1)], function(err, info) {
				if (err) {
					console.log(err);
				}
				
				connection.release();
			});
		});
	});
}

function cbDHT(Type, GPIO, callback) {
	var callbackString = {};
	
	callbackString.temperature = 0;
	callbackString.humidity = 0;
	
	sensorDHT.read(Type, GPIO, function(err, temperature, humidity) {
		if (!err) {
			callbackString.temperature = temperature;
			callbackString.humidity = humidity;
		}
		
		callback(err, callbackString);
	});
}


//---------------------------------------------------------------------------
// DS
//---------------------------------------------------------------------------
function DS(Id, SerialNo) {
	
	//var temp = sensorDS.temperatureSync(SerialNo);
	
	sensorDS.temperature(SerialNo, function(err, value) {
		if (err) {
			console.log(err);
			return;
		}
		
		// Update database
		mysql.getConnection(function(err, connection) {
			connection.query("INSERT INTO cr_sensors_log (LogSensorId, LogDate, LogValue1) VALUES (?, NOW(), ?)", [Id, value], function(err, info) {
				if (err) {
					console.log(err);
				}
	
				connection.release();
			});
		});
	});
}

function cbDS(SerialNo, callback) {
	
	sensorDS.temperature(SerialNo, function(err, value) {
		callback(err, value);
	});
}


//---------------------------------------------------------------------------
// TSL2561
//---------------------------------------------------------------------------
function TSL(Id) {
	
	var sens = new sensorTSL();
	
	sens.init(function(err, val) {
		if (err) {
			console.log('Init error:', error);
		} else {
    		sens.getLux(function(error, val) {
				if (error) {
					console.log('Sensor error:', error);
				} else {
					// Update database
					mysql.getConnection(function(err, connection) {
						if (err) {
							console.log(err);
							return;
						}
						
						connection.query("INSERT INTO cr_sensors_log (LogSensorId, LogDate, LogValue1) VALUES (?, NOW(), ?)", [4, val.toFixed(0)], function(err, info) {
							if (err) {
								console.log(err);
							}
				
							connection.release();
						});
					});
				}
			});
		}
	});  
}


function cbTSL(Id, callback) {

	var sens = new sensorTSL();
	
	sens.init(function(err, val) {
		if (err) {
			callback(err, 0);
			return;
		}

		sens.getLux(function(error, val) {
			if (error) {
				callback(err, 0);
			} else {
				callback(err, val.toFixed(0));
			}
		});
	});
}

//---------------------------------------------------------------------------
// LDR
//---------------------------------------------------------------------------
function LDR(Id, GPIO) {
	//console.log('LDR...');
}


//---------------------------------------------------------------------------
// GetSingleStatus
//---------------------------------------------------------------------------
function GetSingleStatus(nId, callback) {	
	
	// Get sensor
	mysql.getConnection(function(err, connection) {
		connection.query('SELECT SensorId, SensorName, SensorType, SensorGPIO, SensorSerialNo FROM cr_sensors WHERE SensorId = ?', [nId], function(err, rows, fields) {
			if (err) {
				console.log(err);
				callback(err, false);
			} else if (rows.length < 1) {
				console.log('Sensor with id', nId, 'not found! (GetSingleStatus)');
				callback('Not found', false);
			} else {
				switch(rows[0].SensorType) {
					case "DHT11":
						cbDHT(11, Number(rows[0].SensorGPIO), function(err, result) {
							callback(err, result);
						});
						
						break;
						
					case "DHT22":
						cbDHT(22, Number(rows[0].SensorGPIO), function(err, result) {
							callback(err, result);
						});
												
						break;
						
					case "DS1822":
					case "DS18S20":
					case "DS18B20":
					case "MAX31850K":
						cbDS(rows[0].SensorSerialNo, function(err, result) {
							callback(err, result);
						});
					
						//callback(err, sensorDS.temperatureSync(rows[0].SensorSerialNo));
						break;
						
					case "TSL2561":
						cbTSL(Number(rows[0].SensorSerialNo), function(err, result) {
							callback(err, result);
						});
												
						break;
						
					case "LDR":
						callback(err, 0); break;
						
					default:
						callback(err, 0); break;
				}
			}
			
			connection.release();
		});
	});
}


//---------------------------------------------------------------------------
// Read all
//---------------------------------------------------------------------------
function readAll() {
	
	mysql.getConnection(function(err, connection) {
		connection.query('SELECT SensorId, SensorName, SensorType, SensorGPIO, SensorSerialNo FROM cr_sensors WHERE SensorLog=1 ORDER BY SensorId ASC', function(err, rows, fields) {
			if (err) {
				console.log(err);
				connection.release();
				return;
			}


			for (var i = 0; i<rows.length; i++) {
				var row = rows[i];
				
				switch(row.SensorType) {
					case "DHT11":
						DHT(row.SensorId, 11, Number(row.SensorGPIO)); break;
						
					case "DHT22":
						DHT(row.SensorId, 22, Number(row.SensorGPIO)); break;
						
					case "DS1822":
					case "DS18S20":
					case "DS18B20":
					case "MAX31850K":
						DS(row.SensorId, row.SensorSerialNo); break;
						
					case "TSL2561":
						TSL(Number(rows[0].SensorGPIO)); break;
						
					case "LDR":
						LDR(row.SensorId, Number(row.SensorGPIO)); break;
						
					default:
						console.log("Unknown sensor type for", row.SensorName); break;
				}
			}
			
			connection.release();
		});
	});
}


//---------------------------------------------------------------------------
// Module export
//---------------------------------------------------------------------------
var self = module.exports = {

	readAll: function() {
		readAll();
	},
	
	getSingleStatus: function(nId, callback) {
		return GetSingleStatus(nId, callback);
	}

};