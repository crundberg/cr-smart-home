// BASE SETUP
// =============================================================================

var express = require('express');
var mysql = require('./../../mysql.js');
var lamps = require('./../lamps.js');

// ROUTES FOR OUR API
// =============================================================================
var router = express.Router();

/**
 * @apiDefine LampSuccess
 * @apiSuccess {Number} LampId			Lamp unique ID
 * @apiSuccess {Number} LampRoomId		The room ID that light belongs to
 * @apiSuccess {String} LampName		Lamp name
 * @apiSuccess {String} LampType		Type of lamp 
 * @apiSuccess {Number} LampPowerOn		Lamp is powered on
 * @apiSuccess {Number} LampPowerOnMan	Lamp is powered on manually
 * @apiSuccess {Number} LampCmdOn		RF command to power on lamp
 * @apiSuccess {Number} LampCmdOff		RF command to power off lamp
 * @apiSuccess {Number} LampInInAll		Include lamp i power all on or off
 * @apiSuccess {Number} LampOrder		Number to sort the lights ascending
 */
 
/** 
 * @apiDefine LampParam
 * @apiParam {Number} LampRoomId		The room ID that light belongs to
 * @apiParam {String} LampName			Lamp name
 * @apiParam {String} LampType			Type of lamp 
 * @apiParam {Number} LampPowerOn		Lamp is powered on
 * @apiParam {Number} LampPowerOnMan	Lamp is powered on manually
 * @apiParam {Number} LampCmdOn			RF command to power on lamp
 * @apiParam {Number} LampCmdOff		RF command to power off lamp
 * @apiParam {Number} LampInInAll		Include lamp i power all on or off
 * @apiParam {Number} LampOrder			Number to sort the lights ascending
 */


/**
 * @api {get} /lamps/ Request all lamps
 * @apiName GetLamps
 * @apiGroup Lamps
 *
 * @apiUse LampSuccess
 *
 * @apiSuccessExample {json} Success-Response:
 *     HTTP/1.1 200 OK
 *     "lamps": [
 *     {
 *       "LampId": 1,
 *       "LampRoomId": null,
 *       "LampName": "Hall",
 *       "LampType": "Nexa",
 *       "LampPowerOn": 1,
 *       "LampPowerOnMan": 1,
 *       "LampCmdOn": "262165",
 *       "LampCmdOff": "262164",
 *       "LampIncInAll": 1,
 *       "LampOrder": 1
 *     },
 *     {
 *       "LampId": 2,
 *       "LampRoomId": 1,
 *       "LampName": "Window",
 *       "LampType": "Nexa",
 *       "LampPowerOn": 0,
 *       "LampPowerOnMan": 1,
 *       "LampCmdOn": "278549",
 *       "LampCmdOff": "278548",
 *       "LampIncInAll": 1,
 *       "LampOrder": 2
 *     }
 *  ]
 */
router.get('/lamps', function(req, res) {
	mysql.getConnection(function(err, connection) {
		connection.query('SELECT * FROM cr_lamp_objects ORDER BY LampOrder', function(err, rows, fields) {
			if (err) {
				console.log(err);
				res.json({ error: err });
			} else {
				res.json({ lamps: rows });
			}
			
			connection.release();
		});
	});
});


/**
 * @api {get} /lamps/:id Request a single lamp
 * @apiName GetSingleLamp
 * @apiGroup Lamps
 *
 * @apiParam {Number} id Lamp unique ID.
 *
 * @apiUse LampSuccess
 *
 * @apiSuccessExample {json} Success-Response:
 *     HTTP/1.1 200 OK
 *     "lamps": [
 *     {
 *       "LampId": 1,
 *       "LampRoomId": null,
 *       "LampName": "Hall",
 *       "LampType": "Nexa",
 *       "LampPowerOn": 1,
 *       "LampPowerOnMan": 1,
 *       "LampCmdOn": "262165",
 *       "LampCmdOff": "262164",
 *       "LampIncInAll": 1,
 *       "LampOrder": 1
 *     }
 *  ]
 */
router.get('/lamps/:LampId', function(req, res) {
	mysql.getConnection(function(err, connection) {
		connection.query('SELECT * FROM cr_lamp_objects WHERE LampId=?', req.params.LampId, function(err, rows, fields) {
			if (err) {
				console.log(err);
				res.json({ error: err });
			} else if (rows.length < 1) {
				res.status(204).send({ error: 'No Content' })
			} else {
				res.json({ lamps: rows });
			}
			
			connection.release();
		});
	});
});


/**
 * @api {post} /lamps/ Insert a new lamp
 * @apiName InsertLamp
 * @apiGroup Lamps
 *
 * @apiUse LampParam
 *
 * @apiSuccessExample {json} Success-Response:
 *     HTTP/1.1 200 OK
 *     "message": "Lamp inserted!"
 */
router.post('/lamps/', function(req, res) {
	
	var post  = {
		LampRoomId: req.body.roomId,
		LampName: req.body.name,
		LampType: req.body.type,
		LampCmdOn: req.body.cmdOn,
		LampCmdOff: req.body.cmdOff,
		LampIncInAll: req.body.incInAll,
		LampOrder: req.body.order
	};
	
	mysql.getConnection(function(err, connection) {		
		connection.query('INSERT INTO cr_lamp_objects SET ?', post, function(err, result) {
			if (err) {
				console.log(err);
				res.json({ error: err });
			} else {
				res.json({ message: 'Lamp inserted!' });
			}
			
			connection.release();
		});
	});
});


/**
 * @api {put} /lamps/ Update a lamp
 * @apiName UpdateLamp
 * @apiGroup Lamps
 *
 * @apiParam {Number} id Lamp unique ID.
 * @apiUse LampParam
 *
 * @apiSuccessExample {json} Success-Response:
 *     HTTP/1.1 200 OK
 *     "message": "Lamp updated!"
 */
router.put('/lamps/:LampId', function(req, res) {
	
	var post = {};
	
	if (req.body.roomId != undefined) {
		post.LampRoomId = (req.body.roomId == '') ? null : req.body.roomId;
	}
	
	if (req.body.name != undefined) {
		post.LampName = req.body.name;
	}
	
	if (req.body.type != undefined) {
		post.LampType = req.body.type;
	}
	
	if (req.body.cmdOn != undefined) {
		post.LampCmdOn = req.body.cmdOn;
	}
	
	if (req.body.cmdOff != undefined) {
		post.LampCmdOff = req.body.cmdOff;
	}
	
	if (req.body.incInAll != undefined) {
		post.LampIncInAll = req.body.incInAll;
	}
	
	if (req.body.order != undefined) {
		post.LampOrder == req.body.order;
	}
	
	mysql.getConnection(function(err, connection) {		
		connection.query('UPDATE cr_lamp_objects SET ? WHERE LampId=?', [post, req.params.LampId], function(err, result) {
			if (err) {
				console.log(err);
				res.json({ error: err });
			} else {
				res.json({ message: 'Lamp updated!' });
			}
			
			connection.release();
		});
	});
});


/**
 * @api {delete} /lamps/ Delete a lamp
 * @apiName DeleteLamp
 * @apiGroup Lamps
 *
 * @apiParam {Number} id Lamp unique ID.
 *
 * @apiSuccessExample {json} Success-Response:
 *     HTTP/1.1 200 OK
 *     "message": "Lamp deleted!"
 *
 * @apiErrorExample {json} Error-Response:
 *     HTTP/1.1 404 Not Found
 *     {
 *       "error": "LampNotFound"
 *     }
 */
router.delete('/lamps/:LampId', function(req, res) {
	
	mysql.getConnection(function(err, connection) {		
		connection.query('DELETE FROM cr_lamp_objects WHERE LampId=?', req.params.LampId, function(err, result) {
			if (err) {
				console.log(err);
				res.json({ error: err });
			} else {
				if (result.affectedRows > 0) {
					res.json({ message: 'Lamp deleted!' });
				} else {
					res.json({ message: 'No lamp found!' });
				}
			}
			
			connection.release();
		});
	});
});


/**
 * @api {post} /lamps/action/:LampId Send power to a lamp
 * @apiName PowerLamp
 * @apiGroup Lamps
 *
 * @apiParam {Number} LampId Lamp unique ID.
 * @apiParam {Boolean} value Send power on or off to lamp
 *
 * @apiSuccessExample {json} Success-Response:
 *     HTTP/1.1 200 OK
 *     "message": "Action sent to lamp!"
 *
 * @apiErrorExample {json} Error-Response:
 *     HTTP/1.1 404 Not Found
 *     {
 *       "error": "Value must be a boolean!"
 *     }
 */
router.post('/lamps/action/:LampId', function(req, res) {
	var value = req.body.value;
	
	if (value == 'true' || value == 'false') {
		lamps.powerSingle(req.params.LampId, (value === 'true'));
		res.json({ message: 'Action sent to lamp!' });
	} else {
		res.json({ message: 'Value must be a boolean!' });
	}
});

module.exports = router;