# pixelpi
Games and Animations on 16x16 LEDs

![16x16 LED matrix](https://i.imgur.com/jsguEYEl.jpg)

This is a collection of python scripts that run animations and 
games on a 16x16 matrix of WS2812B LEDs (aka Neopixel, if from Adafruit).
The project is inspired by and compatible to Jeremy Williams' [Game Frame](http://ledseq.com).

[more pictures by @marian42_](https://imgur.com/a/Ql25S)


### LED strips
I recommend you use [this tutorial](https://learn.adafruit.com/neopixels-on-raspberry-pi/overview) to set up the LED hardware.
Make sure you install [rpi_ws281x](https://github.com/jgarff/rpi_ws281x.git) as explained in the tutorial.

#### expected LED strip layout:

```
-> -> -> -> -> -> -> -> -> -> -> -> -> -> -> ->
<- <- <- <- <- <- <- <- <- <- <- <- <- <- <- <-
-> -> -> -> -> -> -> -> -> -> -> -> -> -> -> ->
...
```


### Animations
Place your animations in a folder called `animations` in the repository. For each animation, a file `/animations/animation_name/0.bmp` should exist.

Here are the [Eboy animations](http://ledseq.com/product/game-frame-sd-files/) and a [forum for fan-made Game Frame animations](http://ledseq.com/forums/forum/game-frame/game-frame-art/).
