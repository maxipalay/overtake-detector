const express = require('express');
//const db = require('../mongoose');
const router = express.Router();
const path = require('path');
const mysql = require('mysql');
router.use(function timeLog(req, res, next) {
    next();
});
var conn = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : '',
  database: 'unasev'
});
const util = require('util');
const query = util.promisify(conn.query).bind(conn);
conn.connect(function (err) {
    if (err) {
        console.log('Error connecting to Database',err);
        return;
    }
    console.log('Connection established');
});

(async function () {
   
    router.put('/guardar', async (req, res) => {
	infractions = JSON.parse("["+req.body.infractions+"]")
	try {
		for (i=0;i<infractions.length;i++){
			infraction = infractions[i]
			await query('INSERT INTO registros (matricula,longitud,latitud,velocidad,fecha,hora) VALUES (\"'+infraction.plate+'\",'+parseFloat(infraction.lon)+','+parseFloat(infraction.lat)+','+parseFloat(infraction.vel)+',\''+infraction.dat+'\',\''+infraction.tim+'\');');
                	var lastId = await   query('SELECT LAST_INSERT_ID();');
			await query('INSERT INTO fotos VALUES(\"'+infraction.img+'\",'+lastId[0]['LAST_INSERT_ID()']+');');
		}	
		res.status(200).json({ message: 'datos guardados' });
        } catch (err) {
		console.log(err);
		res.status(400).end();
        }
    });


    router.get('/matricula/:id', async (req, res) => {  
    
        try {
            let deta = await query('SELECT id,matricula,longitud,latitud,velocidad,fecha,hora FROM registros WHERE matricula = '+"\'"+req.params.id+"\';");
            res.send({ data:deta });
            res.end();
        } catch (err) {
            console.log(err);
            res.status(400).json({ message: 'Error del servidor' });
        }
    });
    router.get('/fotos/:id', async (req, res) => {  
    
        try {
            let deta = await query('SELECT foto FROM fotos WHERE id_registro = '+"\'"+req.params.id+"\';");
            res.send({ data:deta });
            res.end();
        } catch (err) {
            console.log(err);
            res.status(400).json({ message: 'Error del servidor' });
        }
    });
    
  
})();
module.exports = router;
