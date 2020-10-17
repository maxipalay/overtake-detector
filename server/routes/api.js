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
        params =req.body.ejemplo_payload
  
        params =params.split("},")
        try {
            for(i=0;i<params.length-1;i++){
                var obj = JSON.parse(params[i].split("},")[0]+"}")
                await query('INSERT INTO registros (matricula,longitud,latitud,velocidad,fecha,hora) VALUES (\"'+obj.matricula+'\",'+parseFloat(obj.longitud)+','+parseFloat(obj.latitud)+','+parseFloat(obj.velocidad)+','+obj.fecha+','+obj.hora+');')
                var lastId = await   query('SELECT LAST_INSERT_ID();')
            
                await query('INSERT INTO fotos VALUES(\"'+obj.foto+'\",'+lastId[0]['LAST_INSERT_ID()']+');')
                }
        //    await db.updateUser(req.params.id, req.body);
            res.status(200).json({ message: 'Usuario actualizado' });
        } catch (err) {
            console.log(err);
            res.status(400).end();
        }
    });


    router.get('/matricula/:id', async (req, res) => {  
    
        try {
            let deta = await query('SELECT id,matricula,longitud,latitud,velocidad,fecha,hora FROM registros WHERE matricula = '+"\'"+req.params.id+"\';");
            console.log(deta)
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
            console.log(deta)
            res.send({ data:deta });
            res.end();
        } catch (err) {
            console.log(err);
            res.status(400).json({ message: 'Error del servidor' });
        }
    });
    
  
})();
module.exports = router;