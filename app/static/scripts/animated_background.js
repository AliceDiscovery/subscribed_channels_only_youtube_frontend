let secret_mode = false;

function onKonamiCode(cb) {
    var input = '';
    var key = '38384040373937396665';
    document.addEventListener('keydown', function (e) {
      input += ("" + e.keyCode);
      if (input === key) {
        return cb();
      }
      if (!key.indexOf(input)) return;
      input = ("" + e.keyCode);
    });
}
  
onKonamiCode(function () {
    secret_mode = true;
})



const canvas = document.querySelector('canvas');
const c = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

var frame_num = 0;
var color_index = 0

const default_speed = 0.2; // In seconds

const default_colors = [
    '#007F00',
    '#00FF00',
    '#FFFF00',
    '#FF7F00',
    '#FF0000',
    '#7F007F',
    '#FF00FF',
    '#7F00FF',
    '#0000FF',
    '#007FFF',
    '#00FFFF'
];

const secret_speed = 0.02; // In seconds

const secret_colors = [
    '#5BCEFA',
    '#F5A9B8',
    '#FFFFFF',
    '#F5A9B8'
]


function animate(colors) {
    frame_num = frame_num + 1;
    if (frame_num % 60 == 0) {
        color_index = color_index + 1;
        if (color_index >= colors.length) {
            color_index = 0;
        }
        if (secret_mode) {
            colors = secret_colors;
            color_index = 0;
        }
    }

    c.fillStyle = 'rgba(0, 0, 0, 0.01)';
    c.fillRect(0, 0, canvas.width, canvas.height);

    c.moveTo(0, canvas.height/2);
    c.beginPath();
    for (let i=0; i<canvas.width; i++){
        c.lineTo(i, (canvas.height/2) + (Math.sin((i+frame_num) * 0.01) * ((canvas.height-50) / 2)));
    }
    c.strokeStyle = colors[color_index];
    c.stroke();

    setTimeout(function(){
        animate(colors);
    }, 1000 * (secret_mode ? secret_speed : default_speed));
}

window.addEventListener('resize', function(event) {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}, true);


animate(default_colors);
