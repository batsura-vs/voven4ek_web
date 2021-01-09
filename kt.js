var positions = [0, 0, 0, 0, 0, 0, 0, 0, 0];
var hod = 'red';
var all_h = 0;
var players = ['red', 'green'];
var intel = [];

function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}

function carry(callback, arglist) {
  var thisObj = this;
  return (function () {
    callback.apply(thisObj, arglist)
  });
}

function count(mas, elem) {
  var count = 0;
  for (var i = 0; mas.length > i; i++) {
    if (mas[i] === elem) {
      count++;
    }
  }
  return count
}

function clear() {
  var cla = document.getElementsByClassName('sectors');
  for (var x = 0; cla.length > x; x++) {
    var canv = cla[x].getContext('2d');
    canv.fillStyle = 'white';
    canv.rect(0, 0, cla[x].width, cla[x].height);
    canv.fill();
  }
  positions = [0, 0, 0, 0, 0, 0, 0, 0, 0];
  all_h = 0;
}

function bot() {
  var newArr = positions.slice(0);
  newArr.reverse();
  var l = document.getElementsByClassName('sectors');
  var best;
  var height_score = -1;
  for (var a = 0; intel.length > a; a++) {
    if (JSON.stringify(intel[a].posit) === JSON.stringify(positions)) {
      if (intel[a].score > height_score) {
        height_score = intel[a].score;
        best = intel[a];
      }
    }
  }
  if (height_score < 0) {
    var r = getRandomInt(9);
    while (positions[r] !== 0 && count(positions, 0) > 0) {
      r = getRandomInt(9);
    }
    var obg = {
      score: 0,
      posit: newArr,
      to: r
    }
    intel.push(obg);
    click(r, l[r]);
  } else {
    click(best.to, l[best.to]);
  }
}

function check_win() {
  // 0  1  2
  // 3  4  5
  // 6  7  8
  var sovp = 0;
  var mas = [[0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]]
  for (var play = 2; play > 0; play--) {
    for (var i = 0; mas.length > i; i++) {
      var mas2 = mas[i];
      for (var x = 0; mas2.length > x; x++) {
        if (positions[mas2[x]] === play) {
          sovp++;
        }
      }
      if (sovp === 3) {
        alert('winner: ' + players[play - 1]);
        clear();
        return true;
      }
      sovp = 0;
    }
  }
  return false
}


function click(number1, c) {
  if (positions[number1] === 0) {
    var canv = c.getContext('2d')
    canv.fillStyle = hod;
    canv.rect(0, 0, c.width, c.height);
    canv.fill();
    positions[number1] = players.indexOf(hod) + 1;
    if (hod === 'red') {
      hod = 'green';
    } else {
      hod = 'red';
      bot();
    }
    all_h++;
    if (check_win()) {
    } else {
      if (all_h === 9) {
        alert('Всё ничья!');
        hod = 'red';
        all_h = 0;
        clear();
      }
    }
  } else {
    alert('Поле занято!');
  }
  document.getElementById('playe').innerText = 'Ход игрока: ' + hod;
  document.getElementById('playe').style.color = hod;
}

window.onload = function (e) {
  document.getElementById('playe').innerText = 'Ход игрока: ' + hod;
  document.getElementById('playe').style.color = hod;
  var z = 0;
  for (var i = 0; i < 9; i++) {
    var d = document.getElementById('game');
    var sector = document.createElement('canvas');
    sector.height = (window.innerHeight + window.innerWidth) / 3 / 3.25;
    sector.width = (window.innerHeight + window.innerWidth) / 3 / 3.25;
    sector.style.border = 'solid black 5px';
    sector.onclick = carry(click, [i, sector]);
    sector.className = 'sectors';
    sector.addEventListener("mouseover", function () {
      this.style.border = 'solid blue 5px';
    });
    sector.addEventListener("mouseleave", function () {
      this.style.border = 'solid black 5px';
    });
    d.appendChild(sector);
    z++;
    if (z === 3) {
      d.appendChild(document.createElement('br'));
      z = 0;
    }
  }
  bot();
}

