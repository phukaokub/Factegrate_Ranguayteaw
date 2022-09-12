// create database
const Database = require('better-sqlite3');
const sort_DB = new Database('sortingSystem.sqlite');

sort_DB.exec(
    "CREATE TABLE IF NOT EXISTS sortingSystem (year INT, month INT, day INT, hour INT, min INT, sec INT, section TEXT, color TEXT, status TEXT)"
);

module.exports = sort_DB;