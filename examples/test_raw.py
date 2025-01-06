# test-raw.py - Proof of concept for running the VFD controled by M9202 chipset
#
# example ported from the code published by emsyscode (Jose Luis Monteiro)
# available on the Github  https://github.com/emsyscode/M9202/
#
from machine import Pin
import time

_reset = Pin(Pin.board.GP18, Pin.OUT, value=True ) # Unactive
_cs = Pin( Pin.board.GP14, Pin.OUT, value=True ) # unactiva
_sdata = Pin( Pin.board.GP13, Pin.OUT )
_sck = Pin( Pin.board.GP16, Pin.OUT, value=True )


def cmd_with_stb( a ):
	global _cs, _sdata, _sck
	# send with stb
	#unsigned char transmit = 7; //define our transmit pin
	#unsigned char data = 170; //value to transmit, binary 10101010
	#unsigned char mask = 1; //our bitmask

	data = a
  
	#This send the strobe signal
	# Note: The first byte input at in after the STB go LOW is interpreted as a command!!!
	_cs.value( 0 )
	time.sleep_ms( 1 )
	for _shift in range( 8 ): # iterate through bit mask
		mask = 0b1 << _shift

		_sck.value( 0 ) 
		time.sleep_ms( 1 )
		if (data & mask) > 0: # if bitwise AND resolves to true
			_sdata.value( 1 )
		else: # if bitwise and resolves to false
			_sdata.value( 0 )

		_sck.value( 1 )
		time.sleep_ms(1)
   
	_cs.value( 1 )
	time.sleep_ms( 1 )



# --- MAIN APPLICATION -------------------------------------------------------------
while True:
	_reset.off()
	time.sleep_ms(1)
	_reset.on()
	time.sleep_ms( 300 )

	# set GPO pins to low
	cmd_with_stb( 0b01000000 ) # GP1 & GP2 is bit B0 and B1
	time.sleep_ms( 1 )

	# Configure VFD display (number of grids)
	cmd_with_stb( 0b01100100 ) # (0b01100100); //12 grids  (0b01100111) //15 grids  //bin(01100001) 9grids
	time.sleep_ms( 1 )

	# set DIMM/PWM to value
	cmd_with_stb( (0b01010000) | 7 ) # (0b01010000) | 7); //0 min - 7 max  )(0b01010000)
	time.sleep_ms( 1 )

	# switch off extra "ADRAM"
	cmd_with_stb(0b00110000)
	for i in range( 12 ):
	    cmd_with_stb( 0x20 )
	time.sleep_ms( 1 )
	  
	# test mode: light all
	cmd_with_stb( 0b01110011 )
	time.sleep_ms( 1 )
	  
	time.sleep( 2 )

	# normal mode
	cmd_with_stb( 0b01110000 ) # //((0b01110000); //test off-normal mode on  (0b01110000)
	time.sleep_ms( 1 )
