var express = require('express')
var session = require('express-session')
var bodyParser = require('body-parser')
var path = require('path')

var app = express()

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'static')));

app.get('/', function(request, response){
  response.sendFile(path.join(__dirname +'/main.html'));
});

app.listen(8080);
