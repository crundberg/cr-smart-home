var mysql = require("mysql");
var config = require('./config.json');

// Create MySQL Connection
var pool = mysql.createPool({
	host     : config.DbHost,
	user     : config.DbUser,
	password : config.DbPassword,
	database : config.DbName,
	multipleStatements: true
});

exports.getConnection = function(callback) {
  pool.getConnection(function(err, conn) {
    if(err) {
      return callback(err);
    }
    callback(err, conn);
  });
};