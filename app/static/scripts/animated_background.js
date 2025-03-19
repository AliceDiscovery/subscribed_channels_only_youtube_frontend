// setup canvas
const canvas = document.querySelector('canvas');
const c = canvas.getContext('2d');


// implement canvas resizing
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

window.addEventListener('resize', function(event) {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}, true);


// create class to handle executing animations
class Animator {
    constructor(animationSpeed = 200) {
        this._animationSpeed = animationSpeed;
        this._frameNum = 0;
        this._currentAnimation = null;
        this._isAnimating = false;
    }

    get animationSpeed() {
        return this._animationSpeed;
    }

    set animationSpeed(value) {
        if (value >= 0) {
            this._animationSpeed = value;
        } else {
            console.error("`animationSpeed` must be a greater than 0.");
        }
    }

    get currentAnimation() {
        return this._currentAnimation;
    }

    set currentAnimation(animation) {
        this._currentAnimation = animation;
    }

    get isAnimating() {
        return this._isAnimating;
    }

    _animate() {
        // stop animating if no animation function is provided
        if (this._currentAnimation == null) {
            this._isAnimating = false;
            return;
        }

	// animate frame
        this._currentAnimation(this._frameNum);
        this._frameNum += 1;

	// recurse to animate next frame
        this._isAnimating = true;
        setTimeout(() => {
            this._animate();
        }, this._animationSpeed);
    }

    startAnimation(animation) {
	// tell the animation to stop
	this.stopAnimation();

        // wait for the last frame of the animation to be executed
        if (this._isAnimating) {
            setTimeout(() => {
                this.startAnimation(animation);
            }, 50);
        }
	
	// start the new animation
	else {
            this.currentAnimation = animation;
            this._frameNum = 0;
            this._animate();
        }
    }

    stopAnimation() {
        this.currentAnimation = null;
    }
}


// use the animator instance to handle running animations
const animator = new Animator();


/*
+==============================+
+ when to change the animation +
+==============================+
*/


function listenForKonamiCode() {
    var input = '';
    // up up down down left right left right b a
    var key = '38384040373937396665';
    document.addEventListener('keydown', function (e) {
        input += ("" + e.keyCode);
        if (input === key) {
	    animator.startAnimation(transFlagSineWaveAnimation);
        }
        if (!key.indexOf(input)) return;
        input = ("" + e.keyCode);
    });
}
  
listenForKonamiCode();


/*
+=====================+
+ animation templates +
+=====================+
*/


function colorSineWaveTemplate(frameNum, colorArray, framesPerColor) {
    const _index = Math.floor(frameNum / 7);

    c.fillStyle = 'rgba(0, 0, 0, 0.01)';
    c.fillRect(0, 0, canvas.width, canvas.height);

    c.moveTo(0, canvas.height/2);
    c.beginPath();
    for (let i=0; i<canvas.width; i++){
        c.lineTo(i, (canvas.height/2) + (Math.sin((i+frameNum) * 0.01) * ((canvas.height-50) / 2)));
    }
    c.strokeStyle = colorArray[_index % colorArray.length];
    c.stroke();
}


/*
+=====================+
+ animation functions +
+=====================+
*/


function rainbowSineWaveAnimation(frameNum) {
    animator.animationSpeed = 200;
    const framesPerColor = 7;

    let colorArray = [
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

    colorSineWaveTemplate(frameNum, colorArray, framesPerColor)
}

function transFlagSineWaveAnimation(frameNum) {
    animator.animationSpeed = 20;
    const framesPerColor = 40;

    let colorArray = [
        '#5BCEFA',
        '#F5A9B8',
        '#FFFFFF',
        '#F5A9B8',
        '#5BCEFA',
	'#000000'
    ];

    colorSineWaveTemplate(frameNum, colorArray, framesPerColor)
}


// play animation on start up
animator.startAnimation(rainbowSineWaveAnimation);
