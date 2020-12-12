from flask import *

app = Flask(__name__, template_folder="/home/voven4ek/IdeaProjects/voven4ek_web")


@app.route('/')
def redactor():
    return '''<!doctype html>
<html lang="en">
<head>
  <title>Phrase-o-matic</title>
  <meta name="viewport" content="width=device-width, maximum-scale=1.0, minimum-scale=1.0">
  <meta charset="utf-8">
</head>
<body>
<canvas width='700px' height='700px' id="board" style="border:1px solid #000000"></canvas>
<script>
//##################################################################
// Variables
//##################################################################
var canvas = document.getElementById('board');
var board = canvas.getContext('2d');
var pen = 1;
var drawing = false;
var place1 = [];
var place2 = [];
var undo = [];
var be_click;

//##################################################################
// Settings
//##################################################################
board.lineWidth = 59;
board.strokeStyle = 'green';
board.lineCap = "round";
canvas.style.cursor = 'crosshair';
canvas.height = window.innerHeight / 100 * 90;
canvas.width = window.innerWidth / 100 * 90;

//##################################################################
// Functions
//##################################################################
function pen1(x, y, dx, dy) {
  board.moveTo(x, y);
  board.lineTo(dx, dy);
  board.stroke();
}


function pen2() {
  var x = place2[0]
  var y = place2[1]
  var dx = place1[0]
  var dy = place1[1]
  board.moveTo(x, y);
  board.lineTo(dx, dy);
  board.stroke();
}


function return_settings() {
  board.lineWidth = 59;
  board.strokeStyle = 'green';
  board.lineCap = "round";
}


function start(mouse) {
  var x = mouse.offsetX;
  var y = mouse.offsetY;
  var dx = x - mouse.movementX;
  var dy = y - mouse.movementY;
  drawing = true;
  board.beginPath();
  if (pen === 2) {
    be_click = canvas.toDataURL('image/png');
    place1 = [x, y, dx, dy];
  }
}


function end(mouse) {
  var x = mouse.offsetX;
  var y = mouse.offsetY;
  var dx = x - mouse.movementX;
  var dy = y - mouse.movementY;
  drawing = false;
  board.closePath();
  place2 = [x, y, dx, dy];
  if (pen === 2) {
    pen2();
  }
}


function draw_canv(x, y, dx, dy) {
  if (drawing) {
    if (pen === 1) {
      pen1(x, y, dx, dy);
    }
    if (pen === 2) {
      var image = new Image();
      image.onload = function() {
        canvas.width = image.width;
        canvas.height = image.height;
        board.drawImage(image, 0, 0, image.width, image.height);
        return_settings();
        var x1 = place1[0];
        var y1 = place1[1];
        pen1(x1, y1, dx, dy);
      };
      image.src = be_click;
    }
  }
}

//##################################################################
// Events
//##################################################################

canvas.onpointermove = function (mouse) {
  var x = mouse.offsetX;
  var y = mouse.offsetY;
  var dx = x - mouse.movementX;
  var dy = y - mouse.movementY;
  draw_canv(x, y, dx, dy);
}

canvas.onpointerdown = start;
canvas.onpointerup = end;

</script>
</body>
</html>'''


if __name__ == '__main__':
    app.run(host='192.168.1.103')