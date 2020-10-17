'use strict';
require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
console.log(process.env.DB_PASS)

//const db = require('./mongoose');
var urlencodedParser = bodyParser.urlencoded({ extended: false, limit: '100mb' })
const apiRouter = require('./routes/api');

const app = express();

app.use ((req, res, next) => {
    var fullUrl = req.protocol + '://' + req.get('host') + req.originalUrl;
    console.log(fullUrl)
    next();
});
(async function () {
    let httpPort = process.env.APP_PORT || 3030;
    let httpPort1 = process.env;
    

    app.use(urlencodedParser);
    app.use(bodyParser.json({ limit: '100mb' }));

    // app.get('/', function (req, res) {
    //     res.sendFile(path.join(__dirname, 'index.html'))
    // })

    app.use(bodyParser.json());
    app.use((req, res, next) => {
        res.set('Access-Control-Allow-Origin', '*');
        res.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE');
        next();
    })

    app.get('/', function (req, res) {
        var fullUrl = req.protocol + '://' + req.get('host') + req.originalUrl;
        console.log(fullUrl)
        res.sendFile(path.join(__dirname, 'www/index.html'))
    })

    
    app.use('/api', apiRouter);

    app.listen(httpPort,"0.0.0.0",function () {
        console.log(httpPort1)
 
        console.log("Listening in port:"+httpPort)
    });
})()