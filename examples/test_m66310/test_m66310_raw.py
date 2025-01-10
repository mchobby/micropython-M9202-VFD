"""
  test_m66310_raw.py raw code for testing the M66310 GPIO expander 

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
import time

_reset = Pin(Pin.board.GP18, Pin.OUT, value=True ) # Unactive
_cs = Pin( Pin.board.GP14, Pin.OUT, value=True ) # VFD unactivated
_sdata = Pin( Pin.board.GP13, Pin.OUT )
_sck = Pin( Pin.board.GP16, Pin.OUT, value=True )

# M66310 GPIO Expander, Latch on raising edge
_latch = Pin( Pin.board.GP20, Pin.OUT, value=True ) 

# Reset
_reset.value( 0 )
time.sleep_ms( 30 )
_reset.value( 1 )


# Activate the groups 1,2,3 so output c,d,e
# Clock out data with  MSBF first
data = 0b0000000000011100

# Shift out the data
for _shift in range( 16 ): #0 to 15
	_mask = 0b1 << (15-_shift)
	_sdata.value( (data & _mask) == _mask )
	# clock it
	_sck.value(0)
	time.sleep_ms(1)
	_sck.value(1)
	time.sleep_ms(1)
# Latch to output
_latch.value(0)
time.sleep_ms(1)
_latch.value(1)
time.sleep_ms(1)

