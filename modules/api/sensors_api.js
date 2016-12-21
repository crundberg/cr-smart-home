// BASE SETUP
// =============================================================================

var express = require('express');
var mysql = require('./../../mysql.js');
var sensors = require('./../sensors.js');

// ROUTES FOR OUR API
// =============================================================================
var router = express.Router();

/**
 * @apiDefine SensorSuccess
 * @apiSuccess {Number} SensorId		Sensor unique ID
 * @apiSuccess {Number} SensorRoomId	The room ID that sensor belongs to
 * @apiSuccess {String} SensorName		Sensor name
 * @apiSuccess {String} SensorType		Type of sensor
 * @apiSuccess {Number} SensorGPIO		I/O number sensor is connected to
 * @apiSuccess {String} SensorSerialNo	Sensor serial number
 * @apiSuccess {Number} SensorOrder		Number to sort sensors ascending
 * @apiSuccess {Number} SensorLog		Log sensor values to database

 */
 
/** 
 * @apiDefine SensorParam
 * @apiParam {Number} SensorRoomId		The room ID that sensor belongs to
 * @apiParam {String} SensorName		Sensor name
 * @apiParam {String} SensorType		Type of sensor
 * @apiParam {Number} SensorGPIO		I/O number sensor is connected to
 * @apiParam {String} SensorSerialNo	Sensor serial number
 * @apiParam {Number} SensorOrder		Number to sort sensors ascending
 * @apiParam {Number} SensorLog			Log sensor values to database
 */


/**
 * @api {get} /sensors/ Request all sensors
 * @apiName GetSensors
 * @apiGroup Sensors
 *
 * @apiUse SensorSuccess
 *
 * @apiSuccessExample {json} Success-Response:
 *     HTTP/1.1 200 OK
 *     {
 *       "sensors": [
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
router.get('/sensors', function(req, res) {
	mysql.getConnection(function(err, connection) {
		connection.query('SELECT * FROM cr_sensors ORDER BY SensorOrder', function(err, rows, fields) {
			if (err) {
				console.log(err);
				res.json({ error: err });
			} else {
				res.json({ sensors: rows });
			}
			
			connection.release();
		});
	});
});


/**
 * @api {get} /sensors/:id Request a single lamp
 * @apiName GetSingleSensor
 * @apiGroup Sensors
 *
 * @apiParam {Number} id Lamp unique ID.
 *
 * @apiUse SensorSuccess
 *
 * @apiSuccessExample {json} Success-Response:
 *     HTTP/1.1 200 OK
 *     {
 *       "sensors": [
 *       {
 *         "SensorId": 1,
 *         "SensorRoomId": 1,
 *         "SensorName": "Indoor",
 *         "SensorType": "DHT22",
 *         "SensorGPIO": 2,
 *         "SensorSerialNo": "",
 *         "SensorOrder": 1,
 *         "SensorLog": 1
 *       }
 *     ]
 *   }
 */
router.get('/sensors/:SensorId', function(req, res) {
	mysql.getConnection(function(err, connection) {
		connection.query('SELECT * FROM cr_sensors WHERE SensorId=?', req.params.SensorId, function(err, rows, fields) {
			if (err) {
				console.log(err);
				res.json({ error: err });
			} else if (rows.length < 1) {
				res.status(204).send({ error: 'No Content' })
			} else {
				res.json({ sensors: rows });
			}
			
			connection.release();
		});
	});
});


/**
 * @api {post} /sensors/ Insert a new sensor
 * @apiName InsertSensor
 * @apiGroup Sensors
 *
 * @apiUse SensorParam
 *
 * @apiSuccessExample {json} Success-Response:
 *     HTTP/1.1 200 OK
 *     "message": "Sensor inserted!"
 */
router.post('/sensors/', function(req, res) {
	
	var post  = {
		SensorRoomId: req.body.roomId,
		SensorName: req.body.name,
		SensorType: req.body.type,
		SensorGPIO: req.body.gpio,
		SensorSerialNo: req.body.serialNo,
		SensorOrder: req.body.order,
		SensorLog: req.body.log,
	};
	
	mysql.getConnection(function(err, connection) {		
		connection.query('INSERT INTO cr_sensors SET ?', post, function(err, result) {
			if (err) {
				console.log(err);
				res.json({ error: err });
			} else {
				res.json({ message: 'Sensor inserted!' });
			}
			
			connection.release();
		});
	});
});


/**
 * @api {put} /sensors/ Update a sensor
 * @apiName UpdateSensor
 * @apiGroup Sensors
 *
 * @apiParam {Number} id Sensor unique ID.
 * @apiUse SensorParam
 *
 * @apiSuccessExample {json} Success-Response:
 *     HTTP/1.1 200 OK
 *     "message": "Sensor updated!"
 */
router.put('/sensors/:SensorId', function(req, res) {
	
	var post = {};
	
	if (req.body.roomId != undefined) {
		post.SensorRoomId = (req.body.roomId == '') ? null : req.body.roomId;
	}
	
	if (req.body.name != undefined) {
		post.SensorName = req.body.name;
	}
	
	if (req.body.type != undefined) {
		post.SensorType = req.body.type;
	}
	
	if (req.body.gpio != undefined) {
		post.SensorGPIO = req.body.gpio;
	}
	
	if (req.body.serialNo != undefined) {
		post.SensorSerialNo = req.body.serialNo;
	}
	
	if (req.body.order != undefined) {
		post.SensorOrder == req.body.order;
	}
	
	if (req.body.log != undefined) {
		post.SensorLog = req.body.log;
	}
	
	mysql.getConnection(function(err, connection) {		
		connection.query('UPDATE cr_sensors SET ? WHERE SensorId=?', [post, req.params.SensorId], function(err, result) {
			if (err) {
				console.log(err);
				res.json({ error: err });
			} else {
				res.json({ message: 'Sensor updated!' });
			}
			
			connection.release();
		});
	});
});


/**
 * @api {delete} /Sensors/ Delete a sensor
 * @apiName DeleteSensor
 * @apiGroup Sensors
 *
 * @apiParam {Number} id Sensor unique ID.
 *
 * @apiSuccessExample {json} Success-Response:
 *     HTTP/1.1 200 OK
 *     "message": "Sensor deleted!"
 *
 * @apiErrorExample {json} Error-Response:
 *     HTTP/1.1 404 Not Found
 *     {
 *       "error": "SensorNotFound"
 *     }
 */
router.delete('/sensors/:SensorId', function(req, res) {
	
	mysql.getConnection(function(err, connection) {		
		connection.query('DELETE FROM cr_sensors WHERE SensorId=?', req.params.SensorId, function(err, result) {
			if (err) {
				console.log(err);
				res.json({ error: err });
			} else {
				if (result.affectedRows > 0) {
					res.json({ message: 'Sensor deleted!' });
				} else {
					res.json({ message: 'SensorNotFound!' });
				}
			}
			
			connection.release();
		});
	});
});


/**
 * @api {get} /sensor/value/:SensorId Get current value from a sensor
 * @apiName SensorValue
 * @apiGroup Sensors
 *
 * @apiParam {Number} SensorId Sensor unique ID.
 *
 * @apiSuccessExample {json} Success-Response:
 *     HTTP/1.1 200 OK
 *     "message": "Action sent to lamp!"
 *
 * @apiErrorExample {json} Error-Response:
 *     HTTP/1.1 404 Not Found
 *     {
 *       "error": "SensorNotFound"
 *     }
 */
router.get('/sensors/value/:SensorId', function(req, res) {
	
	sensors.getSingleStatus(req.params.SensorId, function(err, result) {
		if (err) {
			res.json({ error: true, message: err });
		} else {
			res.json({ success : true, result: result });
		}
	});
});

module.exports = router;