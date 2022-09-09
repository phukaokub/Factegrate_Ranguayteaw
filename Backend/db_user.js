// create database
const Database = require('better-sqlite3');
const user_db = new Database('user.sqlite');

user_db.exec(
    "CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, user TEXT, purple INT, green INT, red INT, blue INT, yellow INT, time TEXT)"
);

module.exports = user_db;