const express = require('express'); // import express package
const app = express();
const PORT = 8080; 

const tele_db = require("./db.js"); // import table

app.use( express.json() ) // use middleware to parse json before response

app.listen(  
    // fire API = listen to specific port
    PORT,
    () => console.log(`it's alive on http://localhost:${PORT}`)
);

app.get('/sorting-system', (request, response) => { 
    // run this function when this route is requested
    const statement = tele_db.prepare(`SELECT * FROM telesorting`);
    const info = statement.all();
    response.json(info);
});

app.post('/sorting-system', (request, response) => { 
    // create new data
    const {year, month, day, hour, min, sec, section, color, status} = request.body;

    const statement = tele_db.prepare(
        "INSERT INTO telesorting (year, month, day, hour, min, sec, section, color, status) VALUES (?,?,?,?,?,?,?,?,?)"
    );

    const info = statement.run(year, month, day, hour, min, sec, section, color, status); // go to ? = placeholder
    response.json(info);
});