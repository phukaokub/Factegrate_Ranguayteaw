// create database
const Database = require('better-sqlite3');
const tele_db = new Database('telesorting.sqlite');

tele_db.exec(
    "CREATE TABLE IF NOT EXISTS telesorting (year INT, month INT, day INT, hour INT, min INT, sec INT, section TEXT, color TEXT, status TEXT)"
);

module.exports = tele_db;