var mysql = require('./../mysql.js');
var config = require('./../config.json');

// Variables
var SunCalc = require('suncalc');
var lat = 57.658274;
var lon = 11.930108;

//---------------------------------------------------------------------------
// Is sun down?
//---------------------------------------------------------------------------
function isSunDown() {
	var now = new Date();
	var times = SunCalc.getTimes(now, lat, lon);
	
	var sunrise = times.sunrise.getTime() + (config.sunriseOffset * 60000);
	var sunset = times.sunset.getTime() + (config.sunsetOffset * 60000);
	
	return (now.getTime() < sunrise || now.getTime() > sunset)
}


//---------------------------------------------------------------------------
// Is sun up?
//---------------------------------------------------------------------------
function isSunUp() {
	var now = new Date();
	var times = SunCalc.getTimes(now, lat, lon);
	
	var sunrise = times.sunrise.getTime() + config.sunriseOffset;
	var sunset = times.sunset.getTime() + config.sunsetOffset;
		
	return (now.getTime() > sunrise || now.getTime() < sunset)
}


//---------------------------------------------------------------------------
// Update database
//---------------------------------------------------------------------------
function updateDb() {
	// Get sunset/sunrise
	var times = SunCalc.getTimes(new Date(), lat, lon);
 	var data = '{"Sunrise":"' + times.sunrise.toLocaleTimeString() + '","Sunset":"' + times.sunset.toLocaleTimeString() + '"}';
		
	// Update database
	mysql.getConnection(function(err, connection) {
		connection.query("INSERT INTO cr_data (DataId, DataName, DataText, DataStatus, DataLastUpdated) VALUES (3, 'Sun', ?, 200, NOW()) ON DUPLICATE KEY UPDATE DataText = VALUES(DataText), DataStatus = VALUES(DataStatus), DataLastUpdated = VALUES(DataLastUpdated)", [data], function(err, info) {
			if (err) {
				console.log(err);
			}

			connection.release();
		});
	});
}


//---------------------------------------------------------------------------
// Export module
//---------------------------------------------------------------------------
var self = module.exports = {

	isSunDown: function() {
		return isSunDown();
	},

	isSunUp: function() {
		return isSunUp();
	},
	
	updateDb: function() {
		updateDb();
	}

};