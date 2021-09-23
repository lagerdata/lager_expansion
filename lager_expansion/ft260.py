from enum import Enum
import hid

FT260_Vid = 0x0403
FT260_Pid = 0x6030


class Flags(Enum):
	FLAG_NONE = 0x00
	FLAG_START = 0x02
	FLAG_REPSTART = 0x03
	FLAG_STOP = 0x04
	FLAG_START_STOP = 0x06

class FT260:
	def __init__(self, vid=None, pid=None, debug=False):
		if vid == None or pid == None:
			self.vid = FT260_Vid
			self.pid = FT260_Pid
		else:
			self.vid = vid
			self.pid = pid
		self.debug = debug
		self.device = hid.device()
		self.device.open(self.vid, self.pid)

	def system_status(self):
		print("System Status")
		rts = self.device.get_feature_report( report_num = 0xA1, max_length = 255 )
		print( [ "%02x" % (each) for each in rts ])

	def i2c_status(self):
		print("I2C Status")
		rts = self.device.get_feature_report( report_num=0xC0, max_length = 255)
		print( [ "%02x" % (each) for each in rts ])

	def write(self, address, flag, data):
		rid = 0xD0
		if len(data) > 4:
			rid = 0xD1
		elif len(data) > 8:
			rid = 0xD2
		elif len(data) > 12:
			rid = 0xD3
		elif len(data) > 16:
			print("Data length error")

		output = [rid, address, flag.value, len(data)]
		output += data
		if self.debug:
			print(f"Writing: \n\tOut: {[ '%02x' % (each) for each in output ]}")
		self.device.write(output)

	def read(self, address, register, length):
		output = [0xD0, address, Flags.FLAG_START.value, 0x01, register]
		if self.debug:
			print("Reading:")
			print(f"\tOut: {[ '%02x' % (each) for each in output ]}")
		self.device.write(output)
		output = [0xC2, address, Flags.FLAG_START_STOP.value, length & 0xFF, (length >> 8) & 0xFF]
		self.device.write(output)
		report = self.device.read(100)
		if self.debug:
			print(f"\tOut: {[ '%02x' % (each) for each in output ]}")
			print(f"\tIn: {[ '%02x' % (each) for each in report ]}")
			print(f"\tResponse: Addr {'0x%02x' % address} Reg {'0x%02x' % register} {['%02x' % (each) for each in report[2:2+length]]}")
		return report[2:2+length]

	def close(self):
		self.device.close()