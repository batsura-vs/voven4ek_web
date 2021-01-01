//##################################################################
// Variables
//##################################################################
var canvas = document.getElementById('board');
var board = canvas.getContext('2d');
var pen = 1;
var style = 'green';
var drawing = false;
var place1 = [];
var place2 = [];
var undo = [];
var be_click;

//##################################################################
// Settings
//##################################################################

//##################################################################
// Functions
//##################################################################
function pen1(x, y, dx, dy) {
  board.moveTo(x, y);
  board.lineTo(dx, dy);
  board.stroke();
}

function Up(id, min) {
  var dis = document.getElementById(id).style.height;
  if (dis === min) {
    document.getElementById(id).style.height = '90%';
  } else {
    document.getElementById(id).style.height = min;
  }
}

function Disp(id) {
  var dis = document.getElementById(id).style.display;
  if (dis === 'none') {
    document.getElementById(id).style.display = 'block';
  } else {
    document.getElementById(id).style.display = 'none';
  }
}

function click(ar) {
  style = ar;
  board.strokeStyle = style;
}

function carry(callback, arglist) {
  var thisObj = this;
  return (function () {
    callback.apply(thisObj, arglist)
  });
}

function load() {
  board.lineWidth = 59;
  board.strokeStyle = 'green';
  board.lineCap = "round";
  canvas.style.cursor = 'crosshair';
  canvas.height = window.innerHeight / 100 * 95;
  canvas.width = window.innerWidth / 100 * 95;
  var palette = document.getElementById('palitra');
  for (var r = 0; r < 255; r += 25) {
    for (var g = 0; g < 255; g += 25) {
      for (var b = 0; b < 255; b += 25) {
        var color = document.createElement('div');
        color.style.backgroundColor = 'rgb(' + r + ', ' + g + ', ' + b + ')';
        color.className = 'pal';
        color.style.height = '10px';
        color.style.width = '10px';
        color.onclick = carry(click, ['rgb(' + r + ', ' + g + ', ' + b + ')']);
        palette.appendChild(color);
      }
    }
  }
}

function change() {
  board.lineWidth = document.getElementById('size').value;
}


function pen2(x, y, dx, dy) {
  var width = document.getElementById('size').value;
  board.globalCompositeOperation = 'destination-out';
  board.strokeStyle = "rgb(255,255,255)"; // зададим белый цвет, чтобы проверить,
  board.lineWidth = width;
  pen1(x, y, dx, dy);
  board.globalCompositeOperation = "source-over";
}


function return_settings() {
  board.lineWidth = document.getElementById('size').value;
  board.strokeStyle = style;
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
  return_settings();
}


function end(mouse) {
  var x = mouse.offsetX;
  var y = mouse.offsetY;
  var dx = x - mouse.movementX;
  var dy = y - mouse.movementY;
  drawing = false;
  board.closePath();
  place2 = [x, y, dx, dy];
}


function draw_canv(x, y, dx, dy) {
  if (drawing) {
    if (pen === 1) {
      pen1(x, y, dx, dy);
    }
    if (pen === 2) {
      var image = new Image();
      image.onload = function () {
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
    if (pen === 3) {
      pen2(x, y, dx, dy);
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

document.addEventListener('keydown', function (key) {
  if (key.code === 'KeyL') {
    pen = 2;
  }
  if (key.code === 'KeyP') {
    pen = 1;
  }
  if (key.code === 'KeyE') {
    be_click = canvas.toDataURL('image/png');
    pen = 3;
  }
});


canvas.onpointerdown = start;
canvas.onpointerup = end;
