import time
from .ft260 import Flags

DAC_REG_DEVID = 0x01
DAC_REG_SYNC = 0x02
DAC_REG_CONFIG = 0x03
DAC_REG_GAIN = 0x04
DAC_REG_TRIGGER = 0x05
DAC_REG_STATUS = 0x07
DAC_REG_DAC = 0x08

DAC_ADDR = 0x48

class DAC80501:
	def __init__(self, device, address=DAC_ADDR):
		self.device = device
		self.address = address
		self.divider = False
		self.buffer_gain = False

	def begin(self):
		self.reset()
		time.sleep(0.01)

	def reset(self):
		self.device.write(self.address, Flags.FLAG_START_STOP, [DAC_REG_TRIGGER, 0x00, 0x0A])

	def get_alarm(self):
		status = self.device.read(self.address, DAC_REG_STATUS, 2)
		return status[1] & 0x01 == True

	def set_gain(self, divider, buffer_gain):
		self.divider = divider
		self.buffer_gain = buffer_gain

		div = 0x01 if divider is True else 0x00
		buf = 0x01 if buffer_gain is True else 0x00

		self.device.write(self.address, Flags.FLAG_START_STOP, [DAC_REG_GAIN, div, buf])

	def set_config(self, reference, power_down):
		ref = 0x00 if reference is True else 0x01
		pwr = 0x01 if power_down is True else 0x00
		self.device.write(self.address, Flags.FLAG_START_STOP, [DAC_REG_CONFIG, ref, pwr])

	def set_value(self, value):
		self.device.write(self.address, Flags.FLAG_START_STOP, [DAC_REG_DAC, (value >> 8) & 0xFF, value & 0xFF])
		# self.device.read(self.address, DAC_REG_DAC, 2)
	
	def set_volts(self, volts):

		volts = 5 if volts > 5 else volts
		volts = 0 if volts < 0 else volts

		vrefio = 2.5
		div = 1 if self.divider is False else 2
		gain = 2 if self.buffer_gain else 1

		dac_data = int(((volts / gain) / (vrefio / div)) * (2**16 - 1))
		print(f"Data: {dac_data} Volts: {volts}")
		self.device.write(self.address, Flags.FLAG_START_STOP, [DAC_REG_DAC, (dac_data >> 8) & 0xFF, dac_data & 0xFF])
