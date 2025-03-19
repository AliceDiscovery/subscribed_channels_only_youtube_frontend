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
            console.error("`animationSpeed` must be a greater than, or equal to 0.");
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
        this._currentAnimation.nextFrame(this._frameNum);
        this._frameNum += 1;

	// recurse to animate next frame
	this._animationSpeed = this._currentAnimation.animationSpeed;
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


class ColorSineWave {
    constructor(colorArray, framesPerColor, numGhostFrames, animationSpeed) {
        this._colorArray = colorArray;
	this._framesPerColor = framesPerColor;
	this._numGhostFrames = numGhostFrames;
	this._animationSpeed = animationSpeed
    }

    get colorArray() {
        return this._colorArray;
    }

    set colorArray(value) {
        this._colorArray = value;
    }

    get framesPerColor() {
        return this._framesPerColor;
    }

    set framesPerColor(value) {
        if (value > 0) {
            this._framesPerColor = value;
        } else {
            console.error("`framesPerColor` must be a greater than 0.");
        }
    }

    get numGhostFrames() {
	return this._numGhostFrames;
    }

    set numGhostFrames(value) {
        if (value > 0) {
            this._numGhostFrames = value;
        } else {
            console.error("`numGhostFrames` must be a greater than 0.");
        }
    }

    get animationSpeed() {
	return this._animationSpeed;
    }

    set animationSpeed(value) {
        if (value > 0) {
            this._animationSpeed = value;
        } else {
            console.error("`animationSpeed` must be a greater than 0.");
        }
    }

    nextFrame(frameNum) {
        c.clearRect(0, 0, canvas.width, canvas.height);
        for (let i=0; i<this._numGhostFrames; i++) {
            let _index = Math.floor((frameNum + i) / this._framesPerColor);

            c.moveTo(0, canvas.height/2);
            c.beginPath();
            for (let j=0; j<canvas.width; j++){
                c.lineTo(j, (canvas.height/2) + (Math.sin((j+i+frameNum) * 0.01) * ((canvas.height-50) / 2)));
            }
            c.strokeStyle = this._colorArray[_index % this._colorArray.length];
            c.stroke();
        }
    }
}


/*
+===================+
+ preset animations +
+===================+
*/


rainbowSineWaveAnimation = new ColorSineWave(
    colorArray = [
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
    ],
    framesPerColor = 7,
    numGhostFrames = 40,
    animationSpeed = 200,
);

transFlagSineWaveAnimation = new ColorSineWave(
    colorArray = [
        '#5BCEFA',
        '#F5A9B8',
        '#FFFFFF',
        '#F5A9B8',
        '#5BCEFA',
	'#000000'
    ],
    framesPerColor = 7,
    numGhostFrames = 107,
    animationSpeed = 60,
);


// play animation on start up
animator.startAnimation(rainbowSineWaveAnimation);
