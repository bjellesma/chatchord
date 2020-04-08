const graphqlHTTP = require('express-graphql'); //graphql api
const { buildSchema } = require('graphql'); //graphql api

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