from smbus2 import SMBus, i2c_msg
import time

base_address = 0xA #Control Code is 1010
start_block = 0x0 #There are 8 256 Word Blocks
address = (base_address << 3) + start_block
start_address = 0x50 #Should be start address at block 0

with SMBus(1) as bus:
	with open('bits.csv','w') as f:
		f.write("Byte Address, Hex, Decimal\n")
		for i in range(3):
			print(i)
			address = address + i
			msg = i2c_msg.write(address,0)
			bus.i2c_rdwr(msg)
			time.sleep(0.1)
			msg = i2c_msg.read(address, 256)
			bus.i2c_rdwr(msg)
			for num_i in range(len(msg)):
				byte_address = str((i*256) + num_i)
				hex_byte = hex(ord(msg.buf[num_i]))
				dec_byte = str(ord(msg.buf[num_i]))
				new_line = byte_address + ',' + hex_byte + ',' + dec_byte + '\n'
				f.write(new_line)
			time.sleep(0.1)