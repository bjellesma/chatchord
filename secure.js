require('dotenv').config()

const dbHost = process.env.DB_HOST;
const dbPort = process.env.DB_PORT;
const dbName = process.env.DB_NAME;
const dbUser = process.env.DB_USER;
const dbPassword = process.env.DB_PASSWORD;

module.exports = {
    dbHost,
    dbPort,
    dbName,
    dbUser,
    dbPassword
}