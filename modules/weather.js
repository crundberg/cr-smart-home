var mysql = require('./../mysql.js');
var config = require('./../config.json');

// Variables
var SMHI = require("smhi-node");
var lat = 57.658274;
var lon = 11.930108;

//---------------------------------------------------------------------------
// Get Weather
//---------------------------------------------------------------------------
function getWeather() {
	SMHI.getForecastForLatAndLong(lat, lon).then(
		function(response) {
			var forecasts = response.getForecasts();
			var nextHour = forecasts[0];
	 
			if (nextHour.getPrecipitationCategory() === SMHI.PrecipitationCategory.RAIN) {
				console.log("It will rain");
			} else {
				console.log("Yay, it won't rain!");
			}
		},
		function(error) {
			console.log("I didn't manage to find out, sorry.", error);
		});
}


//---------------------------------------------------------------------------
// Update database
//---------------------------------------------------------------------------
function updateDb() {
	// Get sunset/sunrise
	var times = SunCalc.getTimes(new Date(), lat, lon);
 	var data = '{"Sunrise":"' + times.sunrise.toLocaleTimeString() + '","Sunset":"' + times.sunset.toLocaleTimeString() + '"}';
		
	// Update database
	mysql.query("INSERT INTO cr_data (DataId, DataName, DataText, DataStatus, DataLastUpdated) VALUES (3, 'Sun', ?, 200, NOW()) ON DUPLICATE KEY UPDATE DataText = VALUES(DataText), DataStatus = VALUES(DataStatus), DataLastUpdated = VALUES(DataLastUpdated)", [data], function(err, info) {
		if (err) {
			console.log(err);
			return;
		}
	});
}


//---------------------------------------------------------------------------
// Export module
//---------------------------------------------------------------------------
var self = module.exports = {

	getWeather: function() {
		return getWeather();
	},
	
	updateDb: function() {
		updateDb();
	}

};