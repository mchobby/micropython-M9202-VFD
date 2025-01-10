"""
  test_m66310.py test the M66310 GPIO expander available on the 
                 Sony CDP-CX350 compact disk player

The MIT License (MIT)
Copyright (c) 2024 Dominique Meurisse, support@mchobby.be, shop.mchobby.be

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""


from machine import Pin
from m66310 import M66310
import time

_reset = Pin(Pin.board.GP18, Pin.OUT, value=True ) # Unactive
_cs = Pin( Pin.board.GP14, Pin.OUT, value=True ) # VFD unactivated
_sdata = Pin( Pin.board.GP13, Pin.OUT )
_sck = Pin( Pin.board.GP16, Pin.OUT, value=True )

# M66310 GPIO Expander, Latch on raising edge
_latch = Pin( Pin.board.GP20, Pin.OUT, value=True ) 

# Modify bits values (as a number)
leds = M66310( _sdata, _sck, _latch, _reset )
leds.data = data = 0b0000000000011100 # 16 bits.
leds.update()
time.sleep_ms( 500 )
leds.clear()
leds.update()

# Update bits by bits
for bit_idx in range( 2, 16 ):
	print( bit_idx )
	leds[bit_idx]=True
	leds.update()
	time.sleep_ms(100)
	leds[bit_idx]=False
	leds.update()
leds.clear()
leds.update()
