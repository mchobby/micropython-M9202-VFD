# Reusing a Sony CDP-CX350 VFD & front panel with Raspberry-Pi Pico and MicroPython
![VFD with M9202 VFD controler](docs/_static/VFD-M9202-intro.png)

The Sony compact disk player CDP-CX350 was a 300 compact disks carrousel + compact disk player.

I did loved that device but he died after too much house move (300 CD does weight a lot). It was in 2005 (20 years before), my wonderful CD player was beyong repair

![CDP-CX350 Sony Compact Disk Player](docs/_static/sony-vdp-vx350.png)

Instead of throwing that piece of technology into the trash, I did salvaged parts and carefully packed the front face.

Nowadays (Jan .2025), I do grab it back to continue my article series about the Vaccum Fluorescent Display.

![CDP-CX350 Sony Compact Disk Player - face plate](docs/_static/sony-vdp-vx350-front-00.jpg)

When looking the back of the PCB of the face plate:

* __Right part__: contains the __VFD display__ on the top and many buttons & LEDs at the bottom.
* __Left part__: contains two rotative button, some additional buttons & LEDs, Play, Pause, Stop buttons.

![CDP-CX350 Sony Compact Disk Player - face plate electronic](docs/_static/sony-vdp-vx350-front-01.jpg)

The main control board here below holds:

* __Top-left__: ribbon interface connector. this will be the main interface to control the panel.
* __Top-center__: a blue connector with wiring to the daugther board.
* __Top-right__: an IR receiver.
* __Vaccurm Fluorescent Display__ : you cannot miss the gorgeous VFD display.
* __Bottom__: contains many buttons and orange LEDs (controled with GPIO extender). The left part expose the on/off button and a RED power led.
* __Very Bottom__: the blue LEDs are IR TRANSMITTER LEDs controled through power transistor. That section have its own blue connector at the bottom of the PCB).

![sony vdp panel - so beautiful](docs/_static/sony-vdp-panel.jpg)

# Interfacing
In this project, I wanted to interface the VFD (Vaccum Fluorescent Display) but also all the buttons, rotary and LEDs... taking the controls of the 2 boards.

![Detail of the main board](docs/_static/sony-vdp-panel-details.jpg)

## About the Vaccum Fluorescent Display (VFD)
It is important to understand how the VFD work before starting some hacking around it.

I Recomend you the reading of the [micropython-M66004-VFD github repository](https://github.com/mchobby/micropython-M66004-VFD). It contains comprehensive informations about how a VFD works.

__Ressources:__

* [M9202 datasheet](docs/MSM9202-01.pdf) - driver of this Vaccum Fluorescent Display. Information behind "-" refer to the Character ROM used.
* __The M9202 specs looks identifcal to the [Princeton Technology PT6203 VFD controler (see this repository)](https://github.com/mchobby/micropython-PT6302-VFD)__.

## VFD interface
The [M9202 datasheet](docs/MSM9202-01.pdf) provides useful informations about control pins.

![M9202 CDP controler pinout](docs/_static/M9202-03-pinout.png)

* __VDD__: Logic voltage in 5V (also work with 3.3V)
* __DA__: DataIn. Send bit by bit with lower significant bit first. 
* __CP__: Clock Pulse. Bit is read on the rising edge.
* __CS__: Chip Select. Set this low to communicates with the controler.
* __Reset__: Put it low to reset the device.
* __FVL__: Negative voltage of the VFD (down to -80 Volts!) to VDD+0.3V

The VFD controler is connected to the Main interface connector __CON1__. 

__Notice:__ many of the controls pins are shared between the VFD controler and the GPIO expander.

![VFD Display interface on CON1](docs/_static/VFD-pcb-pinout.png)

Heather Resistance is 4.80 Ω, so only a low voltage can be applied (about 2.5 to 3V). Under **2.9V, the heater draw 170mA** and provides a clear illumination of the digits. 

The usage of a **VFL voltage of -25V** is good enough to make the VFD working proprely. 

As the PCB doesn't includes the _Bias Cut-off Voltage_ circuitery, we have to make it.

Here is how to wire the Pico on the VFD display

![CDP-CX350 Sony Compact Disk Player - VFD Wiring to Pico](docs/_static/VFD-to-pico.jpg)

The VFD display use all the 16 digits to show characters and the symbols.

It can show 13 + 2 chars on the display. The 16th character is attached to symbols (see the [various examples](examples/)) . The setting one of the two bits of available ADRAM will setup additional symbols.

![CDP CX350 VFD digits](docs/_static/CDP-CX350-VFD-digits.png)

The segments on the Digit #16 controls lot of symbols on the display.

![CDP CX350 VFD Segments of digit #16](docs/_static/CDP-CX350-VFD-digit-16.png)

The remaining of symbols are controled with ADRAM (special RAM that add 2 bits for each Digit#).

![CDP CX350 VFD adram configuration](docs/_static/CDP-CX350-VFD-adram.png)

## LEDs & Buttons interface
As this project focus on the reuse of the complete panel I did also worked oo interfacing with the LEDs and buttons.

* LEDs are controled via the __M66310FP__ 16 bit GPIO Expander + LED controler
* Buttons are read through __ANALOG signals__. Several buttons share a common "key" pin with different pull-down resistor for each of the buttons. That result in a different analog voltage on the "key" pin depending on the pressed button.
* A distinct 5V & GND power circuit is available for the analog operations.

![Keyboard & LED interface](docs/_static/KEYB-pcb-pinout.png)