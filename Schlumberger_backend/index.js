const express = require('express');
const cors = require('cors');
const bodyParser = require("body-parser");
const app = express()
const mysqlConnection = require('./db_connection');
const article = require("./routes/article");
const authentication = require("./routes/authentication");

app.use(cors());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

//API Routes
app.use('/article', article);
app.use('/authentication', authentication);

const port = process.env.PORT || 3000;
app.listen(port, function(err){
    console.log("Server listening on Port", port);
});
