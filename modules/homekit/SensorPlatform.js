var uuid = require('./../../node_modules/hap-nodejs').uuid;
var Accessory = require('./../../node_modules/hap-nodejs').Accessory;
var Service = require('./../../node_modules/hap-nodejs/').Service;
var Characteristic = require('./../../node_modules/hap-nodejs/').Characteristic;
var sensor = require('./../sensors.js');

module.exports = SensorPlatform

function SensorPlatform() {
	this.accessories = [];
}

// Sample function to show how developer can add accessory dynamically from outside event
SensorPlatform.prototype.addAccessory = function(accessoryId, accessoryName, accessoryType) {

	var lightUUID = uuid.generate('hap-nodejs:accessories:sensor' + accessoryId);
	var newAccessory = new Accessory(accessoryName, lightUUID);
	
	newAccessory
		.getService(Service.AccessoryInformation)
		.setCharacteristic(Characteristic.Manufacturer, 'CR Smart Home')
		.setCharacteristic(Characteristic.Model, 'v1.0')
		.setCharacteristic(Characteristic.SerialNumber, '0000000001');
	
	newAccessory.on('identify', function(paired, callback) {
		console.log("Identify the lamp", accessoryName);
		callback();
	});
	
	switch(accessoryType) {
		case "DHT11":
		case "DHT22":
			newAccessory
				.addService(Service.TemperatureSensor, accessoryName)
				.getCharacteristic(Characteristic.CurrentTemperature)
				.on('get', function(callback) {
					
					var err = null;
				    	
					sensor.getSingleStatus(accessoryId, function(err, result) {
						callback(err, result.temperature);
					});
				});
				
			newAccessory
				.addService(Service.HumiditySensor, accessoryName)
				.getCharacteristic(Characteristic.CurrentRelativeHumidity)
				.on('get', function(callback) {
					
					var err = null;
					
					sensor.getSingleStatus(accessoryId, function(err, result) {
						callback(err, result.humidity);
					});
				});

			break;
						
		case "DS1822":
		case "DS18S20":
		case "DS18B20":
		case "MAX31850K":
			newAccessory
				.addService(Service.TemperatureSensor, accessoryName)
				.getCharacteristic(Characteristic.CurrentTemperature)
				.setProps({
				    maxValue: 100,
				    minValue: -100,
				    minStep: 0.01
				})
				.on('get', function(callback) {
					
					var err = null;
				    	
					sensor.getSingleStatus(accessoryId, function(err, result) {
						callback(err, result);
					});
				});
				
			break;
			
		case "TSL2561":
			newAccessory
				.addService(Service.LightSensor, accessoryName)
				.getCharacteristic(Characteristic.CurrentAmbientLightLevel)
				.on('get', function(callback) {
					
					var err = null;
					callback(err, 20);
				    	
					//sensor.getSingleStatus(accessoryId, function(err, result) {
					//	callback(err, result);
					//});
				});
				
			break;
			
		case "LDR":
			newAccessory
				.addService(Service.LightSensor, accessoryName)
				.getCharacteristic(Characteristic.CurrentAmbientLightLevel)
				.on('get', function(callback) {
					
					var err = null;
					callback(err, 20);
				    	
					//sensor.getSingleStatus(accessoryId, function(err, result) {
					//	callback(err, result);
					//});
				});
				
			break;
			
		default:
			console.log('Accessory', accessoryName, 'with id', accessoryId, ' has no accessory type for homekit (' + accessoryType + ')');
			break;
	}


  this.accessories.push(newAccessory);
}