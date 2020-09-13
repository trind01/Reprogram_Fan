from smbus2 import SMBus, i2c_msg
import time
import math

WRITE_SLEEP = 0.05

base_address = 0xA #Control Code is 1010
start_block = 0x0 #There are 8 256 Word Blocks
address = (base_address << 3) + start_block
start_address = 0x50 #Should be start address at block 0

FULL_LED_LINE = 0xF7
LETTER = 5 #bytes Max 18 characters
num_screens = [0] #Number of screens (Max unknown) first byte
screen_bytes = [LETTER,0] #2nd number of chars*5, 3rd line some sort of control ex. controls animation?

#Screen Control Byte
#bit 0 - Erases from the back
#bit 1 - Erases from the front
#bit 2 - Erases from the top
#bit 3 - Stops all animations from appearing
#bit 4 - Unknown
#bit 5 - Write direction 0-L to R, 1-R to L
#bit 6 - Writes from bottom to top
#bit 7 - Write(0) or instantly appear(1)

#Combining the bits will make combination animations but the LEDs get
#get weaker on the fan.

characters = {
    'A' : [0xE0,0xDB,0xBB,0xDB,0xE0],
    'B' : [0xF9,0xC6,0xB6,0xB6,0x80],
    'C' : [0xDD,0xBE,0xBE,0xDD,0xE3],
    'D' : [0xE3,0xDD,0xBE,0xBE,0x80],
    'E' : [0xB6,0xB6,0xB6,0xB6,0x80],
    'F' : [0xBF,0xB7,0xB7,0xB7,0x80],
    'G' : [0xF3,0xB5,0xB6,0xBC,0xC3],
    'H' : [0x80,0xF7,0xF7,0xF7,0x80],
    'I' : [0xBE,0xBE,0x80,0xBE,0xBE],
    'J' : [0x81,0xFE,0xFE,0xFE,0xFD],
    'K' : [0xBE,0xDD,0xEB,0xF7,0x80],
    'L' : [0xFE,0xFE,0xFE,0xFE,0x80],
    'M' : [0x80,0xDF,0xEF,0xDF,0x80],
    'N' : [0x80,0xF9,0xE3,0xCF,0x80],
    'O' : [0xE3,0xDD,0xBE,0xDD,0xE3],
    'P' : [0xCF,0xB7,0xB7,0xB7,0x80],
    'Q' : [0xE2,0xDD,0xBA,0xDD,0xE3],
    'R' : [0xDE,0xAD,0xAB,0xB7,0x80],
    'S' : [0xD9,0xB6,0xB6,0xB6,0xCD],
    'T' : [0xBF,0xBF,0x80,0xBF,0xBF],
    'U' : [0x81,0xFE,0xFE,0xFE,0x81],
    'V' : [0x83,0xFD,0xFE,0xFD,0x83],
    'W' : [0x80,0xFD,0xFB,0xFD,0x80],
    'X' : [0xBE,0xDD,0xE3,0xDD,0xBE],
    'Y' : [0x8F,0xEF,0xE0,0xEF,0x8F],
    'Z' : [0x9E,0xAE,0xB6,0xBA,0xBC],				    
    '0' : [0xC1,0xAE,0xB6,0xBA,0xC1],
    '1' : [0xFF,0xFE,0x80,0xDE,0xFF],
    '2' : [0xCE,0xB6,0xBA,0xBC,0xDE],
    '3' : [0xB9,0x96,0xAE,0xBE,0xBD],
    '4' : [0xFB,0x80,0xDB,0xEB,0xF3],
    '5' : [0xB1,0xAE,0xAE,0xAE,0x8D],
    '6' : [0xF9,0xB6,0xB6,0xD6,0xE1],
    '7' : [0x9F,0xAF,0xB7,0xB8,0xBF],
    '8' : [0xC9,0xB6,0xB6,0xB6,0xC9],
    '9' : [0xC3,0xB5,0xB6,0xB6,0xCF],
    ':' : [0xFF,0xFF,0xC9,0xC9,0xFF],
    '!' : [0xFF,0xFF,0x86,0xFF,0xFF],
    ',' : [0xFF,0xFF,0xF9,0xFA,0xFF],
    '-' : [0xFF,0xF7,0xF7,0xF7,0xFF],
    ' ' : [0xFF,0xFF,0xFF,0xFF,0xFF],
}

def build_screen(screen):
	leds = []
	for char in screen:
		char = char.upper()
		leds.insert(0,characters[char])
		# leds = characters[char] + leds
	return leds
 
def get_control_byte(len_screen):
	if len_screen < 10:
		return 0
	else:
		return 0x84

def invertBits(num):  
    # calculating number of bits  
    # in the number  
    x = int(math.log2(num)) + 1
    # Inverting the bits one by one  
    for i in range(x):  
        num = (num ^ (1 << i))  
    return num

def reverseBits(num,bitSize): 
  
     # convert number into binary representation 
     # output will be like bin(10) = '0b10101' 
     binary = bin(num) 
  
     # skip first two characters of binary 
     # representation string and reverse 
     # remaining string and then append zeros 
     # after it. binary[-1:1:-1]  --> start 
     # from last character and reverse it until 
     # second last character from left 
     reverse = binary[-1:1:-1] 
     reverse = reverse + (bitSize - len(reverse))*'0'
  
     # converts reversed binary string into integer 
     return int(reverse,2) 

for key in characters:
	for i in range(len(characters[key])):
		# print(characters[key])
		characters[key][i] = reverseBits(invertBits(characters[key][i]),8)
		# print(characters[key])



screens =	[
				"Im Ur biggest fan",
				"OH WAIT!",
				"NVM",
				"That dude is an",
				"An absolute Unit",
				"Poop"
			]
index = 0

with SMBus(1) as bus:
	msg = i2c_msg.write(address, [index,len(screens)])
	bus.i2c_rdwr(msg)
	index += 1
	time.sleep(WRITE_SLEEP)

	for screen in screens:
		num_chars = len(screen)
		msg = i2c_msg.write(address, [index,num_chars*5,get_control_byte(num_chars)]) #Set num chars and control
		bus.i2c_rdwr(msg)
		index += 2
		time.sleep(WRITE_SLEEP)
		leds = build_screen(screen)
		for led in leds:
			for l in led:
				data = [index]+[l]
				print(data)
				msg = i2c_msg.write(address, data)
				bus.i2c_rdwr(msg)
				index = index+1
				if index == 256:
					index = 0
					address = address + 1
				time.sleep(WRITE_SLEEP)