// BASE SETUP
// =============================================================================

var express = require('express');
var mysql = require('./../../mysql.js');

// ROUTES FOR OUR API
// =============================================================================
var router = express.Router();

/**
 * @apiDefine ScheduleSuccess
 * @apiSuccess {Number} ScheduleId		Schedule unique ID
 * @apiSuccess {Number} ScheduleLampId	Scheduled lamp ID
 * @apiSuccess {Number} ScheduleWeekday	Day of week
 * @apiSuccess {String} ScheduleTimeOn	Time to power on
 * @apiSuccess {String} ScheduleTimeOff	Time to power off
 * @apiSuccess {String} ScheduleMode	Schedule mode (0=Inactive, 1=On, 2=On if sun is down)
 */
 
/** 
 * @apiDefine ScheduleParam
 * @apiSuccess {Number} ScheduleLampId	Scheduled lamp ID
 * @apiSuccess {Number} ScheduleWeekday	Day of week
 * @apiSuccess {String} ScheduleTimeOn	Time to power on
 * @apiSuccess {String} ScheduleTimeOff	Time to power off
 * @apiSuccess {String} ScheduleMode	Schedule mode (0=Inactive, 1=On, 2=On if sun is down)
 */


/**
 * @api {get} /schedule/ Request all schedules
 * @apiName GetSchedules
 * @apiGroup Schedule
 *
 * @apiUse ScheduleSuccess
 *
 * @apiSuccessExample {json} Success-Response:
 *     HTTP/1.1 200 OK
 *     {
 *       "schedule": [
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
router.get('/schedules', function(req, res) {
	mysql.getConnection(function(err, connection) {
		connection.query('SELECT * FROM cr_lamp_schedule ORDER BY ScheduleId', function(err, rows, fields) {
			if (err) {
				console.log(err);
				res.json({ error: err });
			} else {
				res.json({ schedules: rows });
			}
			
			connection.release();
		});
	});
});


/**
 * @api {get} /schedule/:id Request a single schedule
 * @apiName GetSingleSchedule
 * @apiGroup Schedule
 *
 * @apiParam {Number} id Schedule unique ID.
 *
 * @apiUse ScheduleSuccess
 *
 * @apiSuccessExample {json} Success-Response:
 *     HTTP/1.1 200 OK
 *     {
 *       "schedule": [
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
router.get('/schedules/:ScheduleId', function(req, res) {
	mysql.getConnection(function(err, connection) {
		connection.query('SELECT * FROM cr_lamp_schedule WHERE ScheduleId=?', req.params.ScheduleId, function(err, rows, fields) {
			if (err) {
				console.log(err);
				res.json({ error: err });
			} else if (rows.length < 1) {
				res.status(204).send({ error: 'No Content' })
			} else {
				res.json({ schedules: rows });
			}
			
			connection.release();
		});
	});
});


/**
 * @api {post} /schedules/ Insert a new schedule
 * @apiName InsertSchedule
 * @apiGroup Schedule
 *
 * @apiUse ScheduleParam
 *
 * @apiSuccessExample {json} Success-Response:
 *     HTTP/1.1 200 OK
 *     "message": "Schedule inserted!"
 */
router.post('/schedules/', function(req, res) {
	
	var post  = {
		ScheduleLampId: req.body.lampId,
		ScheduleWeekday: req.body.weekday,
		ScheduleTimeOn: req.body.timeOn,
		ScheduleTimeOff: req.body.timeOff,
		ScheduleMode: req.body.mode
	};
	
	mysql.getConnection(function(err, connection) {		
		connection.query('INSERT INTO cr_lamp_schedule SET ?', post, function(err, result) {
			if (err) {
				console.log(err);
				res.json({ error: err });
			} else {
				res.json({ message: 'Schedule inserted!' });
			}
			
			connection.release();
		});
	});
});


/**
 * @api {put} /schedule/ Update a schedule
 * @apiName UpdateSchedule
 * @apiGroup Schedule
 *
 * @apiParam {Number} id Schedule unique ID.
 * @apiUse ScheduleParam
 *
 * @apiSuccessExample {json} Success-Response:
 *     HTTP/1.1 200 OK
 *     "message": "Schedule updated!"
 */
router.put('/schedules/:ScheduleId', function(req, res) {
	
	var post = {};
	
	if (req.body.lampId != undefined) {
		post.ScheduleLampId = req.body.lampId;
	}
	
	if (req.body.weekday != undefined) {
		post.ScheduleWeekday = req.body.weekday;
	}
	
	if (req.body.timeOn != undefined) {
		post.ScheduleTimeOn = req.body.timeOn;
	}
	
	if (req.body.timeOff != undefined) {
		post.ScheduleTimeOff = req.body.timeOff;
	}

	if (req.body.mode != undefined) {
		post.ScheduleMode = req.body.mode;
	}
	
	mysql.getConnection(function(err, connection) {		
		connection.query('UPDATE cr_lamp_schedule SET ? WHERE ScheduleId=?', [post, req.params.ScheduleId], function(err, result) {
			if (err) {
				console.log(err);
				res.json({ error: err });
			} else {
				res.json({ message: 'Schedule updated!' });
			}
			
			connection.release();
		});
	});
});


/**
 * @api {delete} /Schedule/ Delete a schedule post
 * @apiName DeleteSchedule
 * @apiGroup Schedule
 *
 * @apiParam {Number} id Schedule unique ID.
 *
 * @apiSuccessExample {json} Success-Response:
 *     HTTP/1.1 200 OK
 *     "message": "Schedule deleted!"
 *
 * @apiErrorExample {json} Error-Response:
 *     HTTP/1.1 404 Not Found
 *     {
 *       "error": "ScheduleNotFound"
 *     }
 */
router.delete('/schedules/:ScheduleId', function(req, res) {
	
	mysql.getConnection(function(err, connection) {		
		connection.query('DELETE FROM cr_lamp_schedule WHERE ScheduleId=?', req.params.ScheduleId, function(err, result) {
			if (err) {
				console.log(err);
				res.json({ error: err });
			} else {
				if (result.affectedRows > 0) {
					res.json({ message: 'Schedule deleted!' });
				} else {
					res.json({ message: 'ScheduleNotFound!' });
				}
			}
			
			connection.release();
		});
	});
});


/**
 * @api {get} /schedule/lamp/:id Request schedule for a lamp
 * @apiName GetScheduleForLamp
 * @apiGroup Schedule
 *
 * @apiParam {Number} id Lamp unique ID.
 *
 * @apiUse ScheduleSuccess
 *
 * @apiSuccessExample {json} Success-Response:
 *     HTTP/1.1 200 OK
 *     {
 *       "schedule": [
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
router.get('/schedules/lamp/:ScheduleId', function(req, res) {
	mysql.getConnection(function(err, connection) {
		connection.query('SELECT * FROM cr_lamp_schedule WHERE LampId=? ORDER BY ScheduleWeekday ASC, ScheduleTimeOn ASC', req.params.ScheduleId, function(err, rows, fields) {
			if (err) {
				console.log(err);
				res.json({ error: err });
			} else {
				res.json({ schedules: rows });
			}
			
			connection.release();
		});
	});
});


module.exports = router;