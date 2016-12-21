var rcswitch = require('rcswitch-gpiomem');
var mysql = require('./../mysql.js');
var sun = require('./sun.js');
var config = require('./../config.json');

// Variables
var dtNow
var dtDateNow
var nWeekday
var bSunIsDown
var bPowerOn
var nLastLampId
var dtStart
var dtStop
var isLastRow


//---------------------------------------------------------------------------
// LampPower
//---------------------------------------------------------------------------
function LampPower(nId, sName, PowerOn, nCmd) {
	// Update database
	mysql.getConnection(function(err, connection) {
		connection.query("UPDATE cr_lamp_objects SET LampPowerOn = ?, LampPowerOnMan = ? WHERE LampId = ?", [PowerOn, PowerOn, nId], function(err, info) {
			// Error handling
			if (err) {
				console.log(err);
				connection.release();
				return;
			}
			
			// Log
			console.log('Sending power', PowerOn ? 'on' : 'off', 'command to', sName);
		
			// Send command to lamp
			rcswitch.enableTransmit(config.GPIO_RF);
			rcswitch.send(nCmd, 24)
			
			// Release database connection
			connection.release();
		});
	});
}


//---------------------------------------------------------------------------
// PowerSingle
//---------------------------------------------------------------------------
function PowerSingle(nId, bValue) {
	
	// Get lamp
	mysql.getConnection(function(err, connection) {
		connection.query('SELECT LampName, LampCmdOn, LampCmdOff FROM cr_lamp_objects WHERE LampId = ?', [nId], function(err, rows, fields) {
			// Error handling
			if (err) {
				console.log(err);
				connection.release();
				return;
			}
			
			// No posts found
			if (rows.length < 1) {
				console.log('Lamp with id', nId, 'not found! (PowerSingle)');
				connection.release();
				return;
			}
			
			// Log
			console.log('Sending power', bValue ? 'on' : 'off', 'command to', rows[0].LampName);
			rcswitch.enableTransmit(config.GPIO_RF);
			rcswitch.send(bValue ? Number(rows[0].LampCmdOn) : Number(rows[0].LampCmdOff), 24);
			
			// Release database connection
			connection.release();
		});
	});
	
	// Update database
	mysql.getConnection(function(err, connection) {
		connection.query("UPDATE cr_lamp_objects SET LampPowerOnMan = ? WHERE LampId = ?", [bValue, nId], function(err, info) {
			// Error handling
			if (err) {
				console.log(err);
			}
			
			// Release database connection
			connection.release();
		});
	});
}

//---------------------------------------------------------------------------
// GetSingleStatus
//---------------------------------------------------------------------------
function GetSingleStatus(nId, callback) {	
	
	// Get lamp
	mysql.getConnection(function(err, connection) {
		connection.query('SELECT LampName, LampPowerOn, LampPowerOnMan FROM cr_lamp_objects WHERE LampId = ?', [nId], function(err, rows, fields) {
			if (err) {
				console.log(err);
				callback(err, false);
			} else if (rows.length < 1) {
				console.log('Lamp with id', nId, 'not found! (GetSingleStatus)');
				callback('Not found', false);
			} else {
				callback(err, (rows[0].LampPowerOnMan == 1));
			}
			
			connection.release();
		});
	});
}


//---------------------------------------------------------------------------
// Schedule
//---------------------------------------------------------------------------
function schedule() {
	// DateTime
	dtNow = new Date()
	dtDateNow = dtNow.toLocaleDateString();
	nWeekdayNow = (dtNow.getDay() == 0) ? 6 : dtNow.getDay()-1;
		
	// Init variables
	bSunIsDown = sun.isSunDown();
	bPowerOn = false
	nLastLampId = 0

	// Update database
	mysql.getConnection(function(err, connection) {
		connection.query("Update cr_data SET DataText='OK', DataStatus=200, DataLastUpdated=NOW() WHERE DataName='Schedule'", function(err, info) {
			if (err) {
				console.log(err);
				connection.release();
				return;
			}
		});
		
		connection.release();
	});
	
	mysql.getConnection(function(err, connection) {
		connection.query('CALL CR_GetLampSchedules', function(err, rows, fields) {
			if (err) {
				console.log(err);
				connection.release();
				return;
			}

			nLastLampId = -1;
			
			// Loop result from database
			for (var i = 0; i<rows[0].length; i++) {
				var row = rows[0][i];
				
				// Continue if object were started last loop
				if (nLastLampId == row.LampId && bPowerOn) {
					continue;
				}
						
				// Update variables
				bPowerOn = false;
				nLastLampId = row.LampId;
				isLastRow = (i == rows[0].length-1);
					
				// Calculate DateTime for start and stop
				if (nWeekdayNow == row.ScheduleWeekday) {
					dtStart = new Date(dtDateNow + ' ' + row.ScheduleTimeOn);
					dtStop = new Date(dtDateNow + ' ' + row.ScheduleTimeOff);
				} else {
					dtStart = new Date(dtDateNow + ' ' + row.ScheduleTimeOn);
					dtStop = new Date(dtDateNow + ' ' + row.ScheduleTimeOff);
	
					dtStart.setDate(dtStart.getDate() - 1);
					dtStop.setDate(dtStop.getDate() - 1);
				}
				
				// Add extra day if stop date is over midnight
				if (dtStart > dtStop) {
					dtStop.setDate(dtStop.getDate() + 1);
				}
							
				// Power on object
				if (dtNow > dtStart && dtNow < dtStop && (row.ScheduleMode == 1 || (row.ScheduleMode == 2 && bSunIsDown))) {
					
					bPowerOn = true;
			
					if (row.LampPowerOn != 1) {
						console.log(row.LampName, 'power on');
						LampPower(row.LampId, row.LampName, true, Number(row.LampCmdOn));
					}
				} else if (row.LampPowerOn != 0 && row.ScheduleMode != 0 && (isLastRow || row.LampId != rows[0][i+1].LampId)) {
					console.log(row.LampName, 'power off');
					LampPower(row.LampId, row.LampName, false, Number(row.LampCmdOff))
				}
	
			}
			
			connection.release();
		});
	});
}


//---------------------------------------------------------------------------
// Export module
//---------------------------------------------------------------------------
var self = module.exports = {

	schedule: function() {
		schedule();
	},
	
	powerSingle: function(nId, bValue) {
		PowerSingle(nId, bValue);
	},
	
	getSingleStatus: function(nId, callback) {
		return GetSingleStatus(nId, callback);
	}
	
};