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
router.get('/data', function(req, res) {
	mysql.getConnection(function(err, connection) {
		connection.query('SELECT * FROM cr_data ORDER BY DataId', function(err, rows, fields) {
			if (err) {
				console.log(err);
				res.json({ error: err });
			} else {
				res.json({ data: rows });
			}
			
			connection.release();
		});
	});
});


/**
 * @api {get} /data/:id Request a single data post
 * @apiName GetSingleData
 * @apiGroup Data
 *
 * @apiParam {Number} id Data unique ID.
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
 *       }
 *     ]
 *   }
 */
router.get('/data/:DataId', function(req, res) {
	mysql.getConnection(function(err, connection) {
		connection.query('SELECT * FROM cr_data WHERE DataId=?', req.params.DataId, function(err, rows, fields) {
			if (err) {
				console.log(err);
				res.json({ error: err });
			} else if (rows.length < 1) {
				res.status(204).send({ error: 'No Content' })
			} else {
				res.json({ data: rows });
			}
			
			connection.release();
		});
	});
});


/**
 * @api {post} /data/ Insert a new data post
 * @apiName InsertData
 * @apiGroup Data
 *
 * @apiUse DataParam
 *
 * @apiSuccessExample {json} Success-Response:
 *     HTTP/1.1 200 OK
 *     "message": "Data post inserted!"
 */
router.post('/data/', function(req, res) {
	
	var post  = {
		DataName: req.body.name,
		DataText: req.body.text,
		DataStatus: req.body.status,
		DataLastUpdated: req.body.lastUpdated,
	};
	
	mysql.getConnection(function(err, connection) {		
		connection.query('INSERT INTO cr_data SET ?', post, function(err, result) {
			if (err) {
				console.log(err);
				res.json({ error: err });
			} else {
				res.json({ message: 'Data post inserted!' });
			}
			
			connection.release();
		});
	});
});


/**
 * @api {put} /data/ Update a data post
 * @apiName UpdateData
 * @apiGroup Data
 *
 * @apiParam {Number} id Data unique ID.
 * @apiUse DataParam
 *
 * @apiSuccessExample {json} Success-Response:
 *     HTTP/1.1 200 OK
 *     "message": "Data updated!"
 */
router.put('/data/:DataId', function(req, res) {
	
	var post = {};
	
	if (req.body.name != undefined) {
		post.DataName = req.body.name;
	}
	
	if (req.body.text != undefined) {
		post.DataText = req.body.text;
	}
	
	if (req.body.status != undefined) {
		post.DataStatus = req.body.status;
	}
	
	if (req.body.lastUpdated != undefined) {
		post.DataLastUpdated = req.body.lastUpdated;
	}
	
	mysql.getConnection(function(err, connection) {		
		connection.query('UPDATE cr_data SET ? WHERE DataId=?', [post, req.params.DataId], function(err, result) {
			if (err) {
				console.log(err);
				res.json({ error: err });
			} else {
				res.json({ message: 'Data updated!' });
			}
			
			connection.release();
		});
	});
});


/**
 * @api {delete} /Data/ Delete a data post
 * @apiName DeleteData
 * @apiGroup Data
 *
 * @apiParam {Number} id Data unique ID.
 *
 * @apiSuccessExample {json} Success-Response:
 *     HTTP/1.1 200 OK
 *     "message": "Data deleted!"
 *
 * @apiErrorExample {json} Error-Response:
 *     HTTP/1.1 404 Not Found
 *     {
 *       "error": "DataNotFound"
 *     }
 */
router.delete('/Data/:DataId', function(req, res) {
	
	mysql.getConnection(function(err, connection) {		
		connection.query('DELETE FROM cr_data WHERE DataId=?', req.params.DataId, function(err, result) {
			if (err) {
				console.log(err);
				res.json({ error: err });
			} else {
				if (result.affectedRows > 0) {
					res.json({ message: 'Data deleted!' });
				} else {
					res.json({ message: 'DataNotFound!' });
				}
			}
			
			connection.release();
		});
	});
});

module.exports = router;