from smbus2 import SMBus, i2c_msg
import time
import csv

base_address = 0xA #Control Code is 1010
start_block = 0x0 #There are 8 256 Word Blocks
address = (base_address << 3) + start_block
start_address = 0x50 #Should be start address at block 0

all_bytes = []

with open('restore_bits.csv', 'r', newline='') as f:
  reader = csv.reader(f)
  for row in reader:
  	all_bytes.append(int(row[0]))

with SMBus(1) as bus:
	for block in range(3):
		print(block)
		address = address + block
		for page in range(16):
			start_index = (block*256) + (16*page)
			end_index = (block*256) + (16*page) + 16
			data = [16*page] + all_bytes[start_index:end_index]
			print(data)
			msg = i2c_msg.write(address,data)
			bus.i2c_rdwr(msg)
			time.sleep(0.2)

all_bits = "Byte Address, Hex, Decimal\n"
with SMBus(1) as bus:
	address = start_address
	for i in range(3):
		print(i)
		address = address + i
		msg = i2c_msg.write(address,0)
		time.sleep(0.1)
		bus.i2c_rdwr(msg)
		msg = i2c_msg.read(address, 256)
		bus.i2c_rdwr(msg)
		for num_i in range(len(msg)):
			byte_address = str((i*256) + num_i)
			hex_byte = hex(ord(msg.buf[num_i]))
			dec_byte = str(ord(msg.buf[num_i]))
			new_line = byte_address + ',' + hex_byte + ',' + dec_byte + '\n'
			all_bits = all_bits + new_line

with open('bits.csv','w') as f:
	f.write(all_bits)