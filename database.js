
const MongoClient = require('mongodb').MongoClient; //mongodb backend
const {dbHost, dbPort, dbName, dbUser, dbPassword} = require('./secure.js')
// Connection URL
const url = `mongodb://${dbUser}:${dbPassword}@${dbHost}:${dbPort}/${dbName}`
var _db;

// Use connect method to connect to the Server
// https://stackoverflow.com/questions/24621940/how-to-properly-reuse-connection-to-mongodb-across-nodejs-application-and-module
module.exports = {
  connectToServer: function( callback ) {
    MongoClient.connect( url,  { useNewUrlParser: true }, function( err, client ) {
      _db  = client.db(dbName);
      return callback( err );
    } );
  },

  getDb: function() {
    return _db;
  }
}