"""
  test_custom_char.py test example for the M9202 VFD Driver.
  (driver almost identical to Princeton PT6302)

  - Focus: Create a custom char then and display it on Display!
  - VFD Model: all

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
from vfd_pt63 import VFD_PT6302, RAM5
import time

_reset = Pin(Pin.board.GP18, Pin.OUT, value=True ) # Unactive
_cs = Pin( Pin.board.GP14, Pin.OUT, value=True ) # unactiva
_sdata = Pin( Pin.board.GP13, Pin.OUT )
_sck = Pin( Pin.board.GP16, Pin.OUT, value=True )

vfd =VFD_PT6302( sck=_sck, sdata=_sdata, cs=_cs, reset=_reset, digits=16 )

# We can define 5x7 custom char from RAM0 to RAM7
vfd.define_char( RAM5,[
		0b00000,
		0b01010,
		0b10101,
		0b10001,
		0b01010,
		0b00100,
		0b00000 ] )


# First character on the display is at poisition "Digit 4"
# Display 3 times the custom char.
vfd.display_digit( 4, [ RAM5, RAM5, RAM5 ]  )

