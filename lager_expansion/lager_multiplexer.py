from .ft260 import FT260
from .max14661 import MAX14661

ADDRS = [0x98, 0x9A, 0x9C, 0x9E]
multiplexers = []

CHANNELS = {'A': (0, 'A'), 'B': (0, 'B'), 'C': (1, 'A'), 'D': (1, 'B'), 'E': (2, 'A'), 'F': (2, 'B'), 'G': (3, 'A'), 'H': (3, 'B')}

class LagerMultiplexer:
    def __init__(self):
        self.i2c = FT260()
        
        for addr in ADDRS:
            multiplexers.append(MAX14661(self.i2c, addr))

    def mux(common, channel):
        mult, mult_common = CHANNELS[common]
        multiplexers[mult].mux(mult_common, channel)

    def get_mux(common, channel):
        mult, mult_common = CHANNELS[common]
        return multiplexers[mult].get_mux(mult_common)

