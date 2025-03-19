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
    constructor(animationSpeed = 1000) {
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
const animator = new Animator(1000);

