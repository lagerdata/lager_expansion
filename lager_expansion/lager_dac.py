from .ft260 import FT260
from .lager_adc import LagerADC
from .dac80501 import DAC80501

class LagerDAC:
    def __init__(self):
        self.dev = FT260()
        self.dac = DAC80501(self.dev)
        self.dac.begin()
        self.dac.set_gain(divider=False, buffer_gain=True)
        self.dac.set_config(reference=True, power_down=False)

        self.adc = LagerADC(self.dev)

        if self.dac.get_alarm():
            print(">>> Ref alarm!")

    def get_current(self):
        # current = (self.adc.read_adc_single_ended(0) - 2.5) * 2.18
        vout = self.adc.read_adc_single_ended(2)
        sensed = self.adc.read_adc_single_ended(3)

        current = (vout - sensed) * 10000

        return current

    def __getattr__(self, func):
        def method(*args):
            method = getattr(self.dac, func)
            method(*args)
        return method

    def close(self):
        self.dev.close()