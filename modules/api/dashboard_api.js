// BASE SETUP
// =============================================================================

var express = require('express');
var mysql = require('./../../mysql.js');

// ROUTES FOR OUR API
// =============================================================================
var router = express.Router();

/**
 * @apiDefine DataSuccess
 * @apiSuccess {Number} DataId			Data unique ID
 * @apiSuccess {String} DataName		Data name
 * @apiSuccess {String} DataText		Saved data
 * @apiSuccess {Number} DataStatus		Status from data
 * @apiSuccess {String} DataLastUpdated	Date when data where last updated


 */
 
/** 
 * @apiDefine DataParam
 * @apiParam {String} DataName		Data name
 * @apiParam {String} DataText		Saved data
 * @apiParam {Number} DataStatus		Status from data
 * @apiParam {String} DataLastUpdated	Date when data where last updated
 */


/**
 * @api {get} /data/ Request all data
 * @apiName GetData
 * @apiGroup Data
 *
 * @apiUse DataSuccess
 *
 * @apiSuccessExample {json} Success-Response:
 *     HTTP/1.1 200 OK
 *     {
 *       "data": [
 *       {
 *         "SensorId": 1,
 *         "SensorRoomId": 1,
 *         "SensorName": "Indoor",
 *         "SensorType": "DHT22",
 *         "SensorGPIO": 2,
 *         "SensorSerialNo": "",
 *         "SensorOrder": 1,
 *         "SensorLog": 1
 *       },
 *       {
 *         "SensorId": 2,
 *         "SensorRoomId": null,
 *         "SensorName": "Outdoor",
 *         "SensorType": "DS18B20",
 *         "SensorGPIO": 17,
 *         "SensorSerialNo": "28-0000072f3122",
 *         "SensorOrder": 2,
 *         "SensorLog": 1
 *       }
 *     ]
 *   }
 */ 
router.get('/dashboard', function(req, res) {
	mysql.getConnection(function(err, connection) {
		
		var query = "";
		query += "SELECT * FROM cr_scenes ORDER BY SceneOrder ASC; ";
		query += "SELECT t1.*, IFNULL(t2.RoomName, 'Lamps') as RoomName, IFNULL(t2.RoomDescription, '') as RoomDescription, IFNULL(t2.RoomOrder, 1000) as RoomOrder FROM cr_lamp_objects t1 LEFT JOIN cr_rooms t2 ON LampRoomId = RoomId ORDER BY -LampRoomId DESC, RoomOrder ASC, LampOrder ASC; ";
		query += "SELECT SensorId, SensorRoomId, SensorName, SensorType, SensorOrder, LogDate, LogValue1, LogValue2 FROM (SELECT * FROM cr_sensors_log ORDER BY LogDate DESC) t1 LEFT JOIN cr_sensors ON SensorId = LogSensorId LEFT JOIN cr_rooms ON RoomId = SensorRoomId GROUP BY LogSensorId; ";
		query += "SELECT * FROM cr_data WHERE DataName='Sun'; ";
		query += "SELECT * FROM cr_data WHERE DataName='Weather'; ";
		
		var rooms = [];
		var lamps = [];
		var lamp = {};
		var nCount = 0
		var nLampCount = 0
		var nLampsOn = 0
		
		connection.query(query, function(err, result, fields) {
			if (err) {
				console.log(err);
				res.json({ error: err });
			} else {
				
				for (var i = 0; i<result[1].length; i++) {
					var row = result[1][i];

					// Add "Entire room" button on top if it's first in the room
					if (row["LampRoomId"] != null && i==0) {
						lamp = {};
						
						lamp.Id = -1;
						lamp.RoomId = row["LampRoomId"]
						lamp.Name = "Entire room"
						lamp.Type = ""
						lamp.PowerOn = 0
						lamp.PowerOnMan = 0
						lamp.CmdOn = "EntireRoom"
						lamp.CmdOff = "EntireRoom"
						lamp.IncInAll = 1
						lamp.Order = 0
						lamps.push(lamp);
						
						nLampCount = nLampCount+1
						nLampsOn = 0
					}
					
					lamp = {};
					lamp.Id = row["LampId"];
					lamp.RoomId = row["LampRoomId"];
					lamp.Name = row["LampName"];
					lamp.Type = row["LampType"];
					lamp.PowerOn = row["LampPowerOn"];
					lamp.PowerOnMan = row["LampPowerOnMan"];
					lamp.CmdOn = row["LampCmdOn"];
					lamp.CmdOff = row["LampCmdOff"];
					lamp.IncInAll = row["LampIncInAll"];
					lamp.Order = row["LampOrder"];
					lamps.push(lamp);
					
					if (row["LampPowerOnMan"] == 1)
						nLampsOn = nLampsOn+1;
					
					nLampCount = nLampCount+1;
					
					
					// Last row or next row is a new room
					if (i+1 == result[1].length || row['LampRoomId'] != result[1][i+1]['LampRoomId']) {
						room = {};
						room.Id = row['LampRoomId'];
						room.Name = row['RoomName'];
						room.Description = row['RoomDescription'];
						room.Order = row['RoomOrder'];
						room.LampCount = nLampCount;
						room.Lamps = lamps;
						rooms.push(room);
		
						// Update entire room to On if a lamps is powered on
						if (row['LampRoomId'] != null && nLampsOn > 0) {
							lamps[0]['PowerOn'] = 1;
							lamps[0]['PowerOnMan'] = 1;
						}
		
						lamps = [];
						nLampCount = 0;
					}
					
					nCount = nCount+1;
				}
				
				res.json({ scenes: result[0], rooms: rooms, sensors: result[2], sun: result[3], weather: result[4] });
			}
			
			connection.release();
		});
	});
});

module.exports = router;