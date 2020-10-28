# TICV-UNASEVI

<p align="center">
<img src="demo-img.png" width="600">
</p>

Repositorio del proyecto UNASEV-I </br>
Federico Abdo, Juan Abu Arab, Maximiliano Palay, Juan Regent </br>
Laboratorio TIC V </br>
Universidad de Montevideo </br>
2020

## Objetivo

Se propone diseñar y poner en funcionamiento un sistema que permita detectar sobrepasos entre vehículos en zonas donde está prohibido sobrepasar.

## Estructura del proyecto

TICV-UNASEVI<br>
&nbsp;&nbsp;&nbsp;&nbsp;    |<br>
&nbsp;&nbsp;&nbsp;&nbsp;    +- alerts - codigo para alertas al conductor<br>
&nbsp;&nbsp;&nbsp;&nbsp;    +- comms - codigo para guardar las infracciones en la Raspberry y posteriormente subir los datos al servidor<br>
&nbsp;&nbsp;&nbsp;&nbsp;    +- cv - codigo relacionado con computer vision<br>
&nbsp;&nbsp;&nbsp;&nbsp;    +- data - las infracciones se van guardando en esta carpeta<br>
&nbsp;&nbsp;&nbsp;&nbsp;    +- gps - codigo relacionado con la obtencion de datos del gps<br>
&nbsp;&nbsp;&nbsp;&nbsp;    +- server - codigo que corre en el servidor<br>
&nbsp;&nbsp;&nbsp;&nbsp;    +- config.py - configuracion de parametros y constantes del programa<br>
&nbsp;&nbsp;&nbsp;&nbsp;    +- global_vars.py - declaracion e inicializacion de variables globales<br>
&nbsp;&nbsp;&nbsp;&nbsp;    +- main.py - programa principal
