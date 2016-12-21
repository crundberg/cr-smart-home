var storage = require('node-persist');
var uuid = require('./node_modules/hap-nodejs').uuid;
var Bridge = require('./node_modules/hap-nodejs').Bridge;
var Accessory = require('./node_modules/hap-nodejs').Accessory;
var Service = require('./node_modules/hap-nodejs/').Service;
var Characteristic = require('./node_modules/hap-nodejs/').Characteristic;

var config = require('./config.json');
var mysql = require('mysql');
var rcswitch = require('rcswitch-gpiomem');
var lamps = require('./modules/lamps.js');
var LampPlatform = require('./modules/homekit/LampPlatform');
var SensorPlatform = require('./modules/homekit/SensorPlatform');


console.log("HAP-NodeJS starting...");

// Initialize our storage system
storage.initSync();

// Start by creating our Bridge which will host all loaded Accessories
var bridge = new Bridge('CR Smart Home', uuid.generate("CR Smart Home"));

// Listen for bridge identification event
bridge.on('identify', function(paired, callback) {
	console.log("CR Smart Home identify");
	callback();
});

// Create MySQL Connection
var connection = mysql.createPool({
	host     : config.DbHost,
	user     : config.DbUser,
	password : config.DbPassword,
	database : config.DbName
});

// Load platform
var platform = new LampPlatform();

// Get all lamps
connection.getConnection(function(err, connection) {
	connection.query('SELECT * FROM cr_lamp_objects ORDER BY LampOrder ASC', function(err, rows, fields) {
		// Error handling
		if (err) {
			console.log(err);
			connection.release();
			return;
		}
	
		// Loop accessories
		for (var i = 0; i<rows.length; i++) {
			var row = rows[i];
			
			platform.addAccessory(row.LampId, row.LampName);
		}
		
		// Get loaded accessories
		var accessories = platform.accessories;
		
		// Add them all to the bridge
		accessories.forEach(function(accessory) {
			bridge.addBridgedAccessory(accessory);
		});
		
		connection.release();
	});
});

// Load platform
var sensorPlatform = new SensorPlatform();

// Get all lamps
connection.getConnection(function(err, connection) {
	connection.query('SELECT * FROM cr_sensors ORDER BY SensorOrder ASC', function(err, rows, fields) {
		// Error handling
		if (err) {
			console.log(err);
			connection.release();
			return;
		}
	
		// Loop accessories
		for (var i = 0; i<rows.length; i++) {
			var row = rows[i];
			
			sensorPlatform.addAccessory(row.SensorId, row.SensorName, row.SensorType);
		}
		
		// Get loaded accessories
		var sensorAccessories = sensorPlatform.accessories;
		
		// Add them all to the bridge
		sensorAccessories.forEach(function(accessory) {
			bridge.addBridgedAccessory(accessory);
		});
		
		connection.release();
	});
});

// Set information
var info = bridge.getService(Service.AccessoryInformation);
info.setCharacteristic(Characteristic.Manufacturer, 'CR Smart Home');
info.setCharacteristic(Characteristic.Model, 'v1.0');
info.setCharacteristic(Characteristic.SerialNumber, '0000000001');

// Publish the Bridge on the local network.
bridge.publish({
	username: "CC:22:3D:E3:CE:F4",
	port: 51826,
	pincode: "031-45-156",
	category: Accessory.Categories.BRIDGE
});
