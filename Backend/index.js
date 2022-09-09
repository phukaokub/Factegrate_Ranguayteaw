const express = require('express'); // import express package
const app = express();
const PORT = 8080; 

const sort_DB = require("./db_tele.js"); // import table
const user_db = require("./db_user.js");

app.use( express.json() ) // use middleware to parse json before response

app.listen(  
    // fire API = listen to specific port
    PORT,
    () => console.log(`it's alive on http://localhost:${PORT}`)
);

app.get('/sorting-system', (request, response) => { 
    // run this function when this route is requested
    const statement = sort_DB.prepare(`SELECT * FROM sortingSystem`);
    const info = statement.all();
    response.json(info);
});

app.get('/user', (request, response) => { 
    // run this function when this route is requested
    const statement = user_db.prepare(`SELECT * FROM user`);
    const info = statement.all();
    response.json(info);
});

app.post('/sorting-system', (request, response) => { 
    // create new data
    const {year, month, day, hour, min, sec, section, color, status} = request.body;

    const statement = sort_DB.prepare(
        "INSERT INTO sortingSystem (year, month, day, hour, min, sec, section, color, status) VALUES (?,?,?,?,?,?,?,?,?)"
    );

    const info = statement.run(year, month, day, hour, min, sec, section, color, status); // go to ? = placeholder
    response.json(info);
});

app.post('/user', (request, response) => { 
    // create new data
    const {id, user, product, time} = request.body;
    const {purple, green, red, blue, yellow} = product;

    const statement = user_db.prepare(
        "INSERT INTO user (id, user, purple, green, red, blue, yellow, time) VALUES (?,?,?,?,?,?,?,?)"
    );

    const info = statement.run(id, user, purple, green, red, blue, yellow, time); // go to ? = placeholder
    response.json(info);
});

// DROP TABLE
app.delete("/sorting-system", (request, response) => {
    const { password } = request.body;
  
    if (password == "tssRGTno1") {
        const statement = sort_DB.prepare("DROP TABLE sortingSystem");
        const info = statement.run();
      
        response.json(info);
    }

});
  
// DROP TABLE
app.delete("/user", (request, response) => {
    const { password } = request.body;
  
    if (password == "tssRGTno1") {
        const statement = user_db.prepare("DROP TABLE user");
        const info = statement.run();
      
        response.json(info);
    }

});