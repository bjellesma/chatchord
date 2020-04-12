const graphqlHTTP = require('express-graphql'); //graphql api
const { buildSchema } = require('graphql'); //graphql api
const connect = require('../database.js')

const getRooms = connect.then((db) => {
  // Get the documents collection
  const collection = db.collection('rooms');
  // Find some documents
  collection.find({}).toArray(function(err, rooms) {
    return rooms
  });
})

var rooms = getRooms(db)
console.log(`rooms: ${JSON.stringify(rooms)}`)

// Construct a schema, using GraphQL schema language
var schema = buildSchema(`
  type Query {
    rooms: [String]
    bots: [String]
  }
`);

// The root provides a resolver function for each API endpoint
var root = {
  rooms: () => {
    return [
        'Warehouse',
        'Bedroom'
    ];
  },
  bots: () => {
      return [
          'Tim',
          'Jeff',
          'John'
      ]
  }
};



module.exports = {
    schema,
    root
}