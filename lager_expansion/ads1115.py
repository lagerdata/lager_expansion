import time
from enum import Enum
from .ft260 import Flags

# ADDRESSES
ADDR0 = 0x48
ADDR1 = 0x49
ADDR2 = 0x4A
ADDR3 = 0x4B

#    POINTER REGISTER
ADS1X15_REG_POINTER_MASK = 0x03      # Point mask
ADS1X15_REG_POINTER_CONVERT = 0x00   # Conversion
ADS1X15_REG_POINTER_CONFIG = 0x01    # Configuration
ADS1X15_REG_POINTER_LOWTHRESH = 0x02 # Low threshold
ADS1X15_REG_POINTER_HITHRESH = 0x03  # High threshold

# CONFIG REGISTER
ADS1X15_REG_CONFIG_OS_MASK = 0x8000 #  OS Mask
ADS1X15_REG_CONFIG_OS_SINGLE = 0x8000 #  Write: Set to start a single-conversion
ADS1X15_REG_CONFIG_OS_BUSY = 0x0000 #  Read: Bit = 0 when conversion is in progress
ADS1X15_REG_CONFIG_OS_NOTBUSY = 0x8000 #  Read: Bit = 1 when device is not performing a conversion

ADS1X15_REG_CONFIG_MUX_MASK = 0x7000 #  Mux Mask
ADS1X15_REG_CONFIG_MUX_DIFF_0_1 = 0x0000 #  Differential P = AIN0, N = AIN1 (default)
ADS1X15_REG_CONFIG_MUX_DIFF_0_3 = 0x1000 #  Differential P = AIN0, N = AIN3
ADS1X15_REG_CONFIG_MUX_DIFF_1_3 = 0x2000 #  Differential P = AIN1, N = AIN3
ADS1X15_REG_CONFIG_MUX_DIFF_2_3 = 0x3000 #  Differential P = AIN2, N = AIN3

ADS1X15_REG_CONFIG_MUX_SINGLE_0 = 0x4000 #  Single-ended AIN0
ADS1X15_REG_CONFIG_MUX_SINGLE_1 = 0x5000 #  Single-ended AIN1
ADS1X15_REG_CONFIG_MUX_SINGLE_2 = 0x6000 #  Single-ended AIN2
ADS1X15_REG_CONFIG_MUX_SINGLE_3 = 0x7000 #  Single-ended AIN3

ADS1X15_REG_CONFIG_PGA_MASK = 0x0E00 #    PGA Mask
ADS1X15_REG_CONFIG_PGA_6_144V = 0x0000 #  +/-6.144V range = Gain 2/3
ADS1X15_REG_CONFIG_PGA_4_096V = 0x0200 #  +/-4.096V range = Gain 1
ADS1X15_REG_CONFIG_PGA_2_048V = 0x0400 #  +/-2.048V range = Gain 2 (default)
ADS1X15_REG_CONFIG_PGA_1_024V = 0x0600 #  +/-1.024V range = Gain 4
ADS1X15_REG_CONFIG_PGA_0_512V = 0x0800 #  +/-0.512V range = Gain 8
ADS1X15_REG_CONFIG_PGA_0_256V = 0x0A00 #  +/-0.256V range = Gain 16

ADS1X15_REG_CONFIG_MODE_MASK = 0x0100 #    Mode Mask
ADS1X15_REG_CONFIG_MODE_CONTIN = 0x0000 #  Continuous conversion mode
ADS1X15_REG_CONFIG_MODE_SINGLE = 0x0100 #  Power-down single-shot mode (default)

ADS1X15_REG_CONFIG_RATE_MASK = 0x00E0 #  Data Rate Mask

ADS1X15_REG_CONFIG_CMODE_MASK = 0x0010 #  CMode Mask
ADS1X15_REG_CONFIG_CMODE_TRAD = 0x0000 #  Traditional comparator with hysteresis (default)
ADS1X15_REG_CONFIG_CMODE_WINDOW = 0x0010 #  Window comparator

ADS1X15_REG_CONFIG_CPOL_MASK = 0x0008 #  CPol Mask
ADS1X15_REG_CONFIG_CPOL_ACTVLOW = 0x0000 #  ALERT/RDY pin is low when active (default)
ADS1X15_REG_CONFIG_CPOL_ACTVHI = 0x0008 #  ALERT/RDY pin is high when active

ADS1X15_REG_CONFIG_CLAT_MASK = 0x0004 #  Determines if ALERT/RDY pin latches once asserted
ADS1X15_REG_CONFIG_CLAT_NONLAT = 0x0000 #  Non-latching comparator (default)
ADS1X15_REG_CONFIG_CLAT_LATCH = 0x0004 #  Latching comparator

ADS1X15_REG_CONFIG_CQUE_MASK = 0x0003 # CQue Mask
ADS1X15_REG_CONFIG_CQUE_1CONV = 0x0000 # Assert ALERT/RDY after one conversions
ADS1X15_REG_CONFIG_CQUE_2CONV = 0x0001 # Assert ALERT/RDY after two conversions
ADS1X15_REG_CONFIG_CQUE_4CONV = 0x0002 # Assert ALERT/RDY after four conversions
ADS1X15_REG_CONFIG_CQUE_NONE = 0x0003 # Disable the comparator and put ALERT/RDY in high state (default)

class Gain(Enum):
    TWOTHIRDS = ADS1X15_REG_CONFIG_PGA_6_144V # +/- 6.144V range (limited to VDD +0.3V max!)
    ONE = ADS1X15_REG_CONFIG_PGA_4_096V
    TWO = ADS1X15_REG_CONFIG_PGA_2_048V
    FOUR = ADS1X15_REG_CONFIG_PGA_1_024V
    EIGHT = ADS1X15_REG_CONFIG_PGA_0_512V
    SIXTEEN = ADS1X15_REG_CONFIG_PGA_0_256V

class DataRate(Enum):
    R_8SPS = 0x0000 #    8 samples per second
    R_16SPS = 0x0020 #   16 samples per second
    R_32SPS = 0x0040 #   32 samples per second
    R_64SPS = 0x0060 #   64 samples per second
    R_128SPS = 0x0080 #  128 samples per second (default)
    R_250SPS = 0x00A0 #  250 samples per second
    R_475SPS = 0x00C0 #  475 samples per second
    R_860SPS = 0x00E0 #  860 samples per second

class ADS1115:
    def __init__(self, device, address, gain, data_rate):
        self.device = device
        self.address = address
        self.gain = gain
        self.data_rate = data_rate

    def convert_volts(self, results):

        fs_range = 0.0
        if (self.gain == Gain.TWOTHIRDS):
            fs_range = 6.144
        elif (self.gain == Gain.ONE):
            fs_range = 4.096
        elif (self.gain == Gain.TWO):
            fs_range = 2.048
        elif (self.gain == Gain.FOUR):
            fs_range = 1.024
        elif (self.gain == Gain.EIGHT):
            fs_range = 0.512
        elif (self.gain == Gain.SIXTEEN):
            fs_range = 0.256

        return results * (fs_range / 32768)

    def read_adc_single_ended(self, channel, raw=False):

        if (channel < 0 or channel > 3):
            return

        if channel == 0:
            channel_mux = ADS1X15_REG_CONFIG_MUX_SINGLE_0
        elif channel == 1:
            channel_mux = ADS1X15_REG_CONFIG_MUX_SINGLE_1
        elif channel == 2:
            channel_mux = ADS1X15_REG_CONFIG_MUX_SINGLE_2
        elif channel == 3:
            channel_mux = ADS1X15_REG_CONFIG_MUX_SINGLE_3

        config = \
        ADS1X15_REG_CONFIG_CQUE_NONE | \
        ADS1X15_REG_CONFIG_CLAT_NONLAT | \
        ADS1X15_REG_CONFIG_CPOL_ACTVLOW | \
        ADS1X15_REG_CONFIG_CMODE_TRAD | \
        ADS1X15_REG_CONFIG_MODE_SINGLE

        # Set PGA/voltage range
        config |= self.gain.value

        # Set data rate
        config |= self.data_rate.value
        config |= channel_mux   
        config |= ADS1X15_REG_CONFIG_OS_SINGLE

        self.device.write(self.address, Flags.FLAG_START_STOP, [ADS1X15_REG_POINTER_CONFIG, (config >> 8) & 0xFF, config & 0xFF])

        while True:
            # print("Waiting...")
            ret = self.device.read(self.address, ADS1X15_REG_POINTER_CONFIG, 2)
            # print(f"Return: {ret}")
            if (((ret[0] << 8) | ret[1]) & 0x8000) != 0:
                break
            time.sleep(0.01)

        results = self.get_last_conversion_results()
        if not raw:
            results = self.convert_volts(results)
        return results

    def get_last_conversion_results(self):
        ret = self.device.read(self.address, ADS1X15_REG_POINTER_CONVERT, 2)
        return (ret[0] << 8) | ret[1]

    
