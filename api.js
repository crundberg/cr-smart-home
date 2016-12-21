// BASE SETUP
// =============================================================================

var express = require('express');
var bodyParser = require('body-parser');
var passport = require('passport');
var BasicStrategy = require('passport-http').BasicStrategy;

// Modules
var mysql = require('./mysql.js');
var config = require('./config.json');
var lamps = require('./modules/api/lamps_api.js');
var sensors = require('./modules/api/sensors_api.js');
var data = require('./modules/api/data_api.js');
var schedules = require('./modules/api/schedule_api.js');
var rooms = require('./modules/api/rooms_api.js');
var dashboard = require('./modules/api/dashboard_api.js');

// Configure app
var app	 = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(passport.initialize());

// Configure port
var port = process.env.PORT || 5000;

// Configure authentication
passport.use(new BasicStrategy(function(username, password, done) {

		mysql.getConnection(function(err, connection) {		
			connection.query('SELECT UserId FROM cr_users WHERE UserName = ? AND UserPassword = SHA2(CONCAT(?, UserSalt), 512)', [username, password], function(err, result) {
				
				if (err) {
					console.log(err);
					connection.release();
					return done(err);
				} else if (result.length != 1) {
					connection.release();
					return done(null, false, { message: 'Incorrect username or password.' });
				} else {
					connection.release();
					return done(null, result);
				} 
			});
		});
	}
));

// ROUTES FOR OUR API
// =============================================================================
var router = express.Router();
var isAuthenticated = passport.authenticate('basic', { session : false });

router.get('/', function(req, res) {
	res.json({ message: 'Welcome to CR Smart Home!' });
});

app.use('/api', isAuthenticated, router);
app.use('/api', isAuthenticated, lamps);
app.use('/api', isAuthenticated, sensors);
app.use('/api', isAuthenticated, data);
app.use('/api', isAuthenticated, schedules);
app.use('/api', isAuthenticated, rooms);
app.use('/api', isAuthenticated, dashboard);

// START THE SERVER
// =============================================================================
app.listen(port);
console.log('Starting API on port', port);