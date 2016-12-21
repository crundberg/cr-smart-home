require('./homekit.js');
require('./api.js');
var lamps = require('./modules/lamps.js');
var sun = require('./modules/sun.js');
var sensors = require('./modules/sensors.js');
var weather = require('./modules/weather.js');

// Variables
var dtNow = new Date();
var lastMin = -1;
var lastHour = -1;
var lastDay = -1;
var bStartup = true;

//---------------------------------------------------------------------------
// Main
//---------------------------------------------------------------------------
function main(){
	dtNow = new Date();
	
	// Run every new minute
	if (lastMin != dtNow.getMinutes()) {
		lastMin = dtNow.getMinutes();
		
		// Lamps
		lamps.schedule();

		// Run every 10 minutes
		if (lastMin % 10 == 0 || bStartup) {
			// Sensors
			sensors.readAll();
			
			// Weather
			//weather.getWeather();
		}
	}

	// Run every new hour	
	if (lastHour != dtNow.getHours()) {
		lastHour = dtNow.getHours();
	}
	
	// Run every new day
	if (lastDay != dtNow.getDate()) {
		lastDay = dtNow.getDate();
		
		// Sun
		sun.updateDb();
	}
	
	bStartup = false;
}

//---------------------------------------------------------------------------
// Start
//---------------------------------------------------------------------------
console.log('Starting CR Smart Home...')
setInterval(main, 1000);