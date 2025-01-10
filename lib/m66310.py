"""
  M66310.py is a micropython module for Mitsubishi M66310 16 bits GPIO expander

The MIT License (MIT)
Copyright (c) 2025 Dominique Meurisse, support@mchobby.be, shop.mchobby.be

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
import time 

class M66310():
	def __init__( self, data_pin, clock_pin, latch_pin, reset_pin = None ):
		self._sdata = data_pin
		self._sck = clock_pin
		self._latch = latch_pin 
		self._reset = reset_pin

		if self._reset != None:
			# Reset
			self._reset.value( 0 )
			time.sleep_ms( 30 )
			self._reset.value( 1 )

		self._data = 0b0 # 16 bits data

	def update( self ):
		# Shift out the data
		for _shift in range( 16 ): #0 to 15
			_mask = 0b1 << (15-_shift)
			self._sdata.value( (self._data & _mask) == _mask )
			# clock it
			self._sck.value(0)
			self._sck.value(1)
		# Latch to output
		time.sleep_ms(1)
		self._latch.value(0)
		self._latch.value(1)


	def clear( self ):
		self._data = 0b0

	@property
	def data( self ):
		return self._data

	@data.setter
	def data( self, value ):
		""" 16 bits values """
		self._data = value

	def __getitem__(self, idx):
		""" get the bit value from 0..15 """
		assert 0<=idx<=15, "Index must be in range 0..15"
		_mask = 0b1 << idx
		return (self._data & _mask)==_mask

	def __setitem__(self, idx, bool_value):
		""" Set the value a given bitget the bit value from 0..15 """
		assert 0<=idx<=15, "Index must be in range 0..15"
		_mask = 0b1 << idx
		if bool_value:
			self._data = self._data | _mask
		else:
			self._data = self._data & (0xFFFF ^ _mask)