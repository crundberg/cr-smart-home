var uuid = require('./../../node_modules/hap-nodejs').uuid;
var Accessory = require('./../../node_modules/hap-nodejs').Accessory;
var Service = require('./../../node_modules/hap-nodejs/').Service;
var Characteristic = require('./../../node_modules/hap-nodejs/').Characteristic;
var lamps = require('./../lamps.js');

module.exports = LampPlatform

function LampPlatform() {
	this.accessories = [];
}

LampPlatform.prototype.addAccessory = function(accessoryId, accessoryName) {

	// Generate a consistent UUID
	var lightUUID = uuid.generate('hap-nodejs:accessories:outlet' + accessoryId);
	
	// Create new accessory
	var newAccessory = new Accessory(accessoryName, lightUUID);
	
	// Set properties
	newAccessory
		.getService(Service.AccessoryInformation)
		.setCharacteristic(Characteristic.Manufacturer, 'CR Smart Home')
		.setCharacteristic(Characteristic.Model, 'v1.0')
		.setCharacteristic(Characteristic.SerialNumber, '0000000001');
	
	// Listen for the "identify" event for this Accessory
	newAccessory.on('identify', function(paired, callback) {
		console.log('Identify the lamp', accessoryName);
		callback();
	});
	
	// Add the actual Lightbulb Service and listen for change events from iOS.
	newAccessory
		.addService(Service.Outlet, accessoryName)
		.getCharacteristic(Characteristic.On)
		.on('set', function(value, callback) {
			console.log('Turning', accessoryName, value ? 'on' : 'off');
			lamps.powerSingle(accessoryId, value);
			callback();
		});
	
	// We want to intercept requests for our current power state so we can query the hardware itself instead of
	// allowing HAP-NodeJS to return the cached Characteristic.value.
	newAccessory
		.getService(Service.Outlet)
		.getCharacteristic(Characteristic.On)
		.on('get', function(callback) {
			
			var err = null; // in case there were any problems
		    	
			lamps.getSingleStatus(accessoryId, function(err, result) {
				callback(err, result);
			});
		});

  this.accessories.push(newAccessory);
}