import time
from enum import Enum
from .ft260 import Flags

PCA9685_MODE1 = 0x00
PCA9685_MODE2 = 0x01
MODE1_RESTART = 0x80
MODE1_SLEEP = 0x10 
MODE1_AI = 0x20
MODE2_OUTDRV = 0x04
PCA9685_PRESCALE = 0xFE
PCA9685_LED0_ON_L = 0x06

FREQUENCY_OSCILLATOR = 25000000

class OutputModes(Enum):
	PCA_PUSH_PULL = 0
	PCA_OPEN_DRAIN = 1

class PCA9685:
	def __init__(self, device, address):
		self.device = device
		self.address = address

	def begin(self):
		self.reset()

	def reset(self):
		self.device.write(self.address, Flags.FLAG_START_STOP, [PCA9685_MODE1, MODE1_RESTART])
		time.sleep(0.01)

	def set_pwm_freq(self, freq):
		prescale =  int((FREQUENCY_OSCILLATOR / (freq * 4096.0)) + 0.5)

		oldmode = 0x00 # todo read
		newmode = (oldmode & ~MODE1_RESTART) | MODE1_SLEEP
		self.device.write(self.address, Flags.FLAG_START_STOP, [PCA9685_MODE1, newmode])
		self.device.write(self.address, Flags.FLAG_START_STOP, [PCA9685_PRESCALE, prescale])
		self.device.write(self.address, Flags.FLAG_START_STOP, [PCA9685_MODE1, oldmode])
		time.sleep(0.01)
		self.device.write(self.address, Flags.FLAG_START_STOP, [PCA9685_MODE1, oldmode | MODE1_RESTART | MODE1_AI])
		time.sleep(0.01)

	def set_output(self, mode):
		if mode == OutputModes.PCA_PUSH_PULL:
			# todo read mode
			self.device.write(self.address, Flags.FLAG_START_STOP, [PCA9685_MODE2, 0x00 | MODE2_OUTDRV])

	def set_pwm_precise(self, num, on, off):
		self.device.write(self.address, Flags.FLAG_START_STOP, [PCA9685_LED0_ON_L + 4 * num, on & 0xFF, (on >> 8) & 0xFF , off & 0xFF, (off >> 8) & 0xFF])

	def set_pwm(self, num, value):
		if value >= 4095:
			self.set_pwm_precise(num, 4096, 0)
		elif value == 0:
			self.set_pwm_precise(num, 0, 4096)
		else:
			self.set_pwm_precise(num, 0, value)
