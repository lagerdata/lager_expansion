from .ft260 import FT260
from .ads1115 import ADS1115, Gain, DataRate, ADDR0, ADDR1, ADDR2, ADDR3

class LagerADC:
    def __init__(self, gain=Gain.TWOTHIRDS, data_rate=DataRate.R_128SPS, debug=False):
        self.dev = FT260(debug=debug)

        if type(gain) != list:
            gain = [gain] * 4
        if type(data_rate) != list:
            data_rate = [data_rate] * 4

        self.adc0 = ADS1115(self.dev, ADDR0, gain[0], data_rate[0])
        self.adc1 = ADS1115(self.dev, ADDR1, gain[1], data_rate[1])
        self.adc2 = ADS1115(self.dev, ADDR2, gain[2], data_rate[2])
        self.adc3 = ADS1115(self.dev, ADDR3, gain[3], data_rate[3])
        self.adcs = [self.adc0, self.adc1, self.adc2, self.adc3]

    def read_adc_single_ended(self, channel, raw=False):
        device = self.adcs[channel // 4]
        local_channel = channel % 4
        return device.read_adc_single_ended(local_channel, raw)

    def close(self):
        self.dev.close()