from .ft260 import FT260
from .max14661 import MAX14661

ADDRS = [0x4c, 0x4d, 0x4e, 0x4f]
multiplexers = []

CHANNELS = {'A': (0, 'B'), 'B': (0, 'A'), 'C': (1, 'A'), 'D': (1, 'B'), 'E': (2, 'B'), 'F': (2, 'A'), 'G': (3, 'A'), 'H': (3, 'B')}

MULT_MAP_INPUTS = [-1, 11, 10, 9, 1, 2, 3, 4, 5, 6, 7, 8, 16, 15, 14, 13, 12]
UPSIDE_DOWN_BOARDS = ['C', 'D', 'G', 'H']

class LagerMultiplexer:
    def __init__(self):
        self.i2c = FT260(debug=False)
        
        for addr in ADDRS:
            multiplexers.append(MAX14661(self.i2c, addr))

    def mux(self, common, channel):
        mult, mult_common = CHANNELS[common]
        print(f"Muxing input {channel} to output {common}")

        if common in UPSIDE_DOWN_BOARDS:
            channel = MULT_MAP_INPUTS[::-1][channel]
        else:
            channel = MULT_MAP_INPUTS[channel]

        print(f"\tActually mult {mult}, input {channel} output {mult_common}")

        multiplexers[mult].mux(mult_common, channel)

    def get_mux(self, common):
        # TODO fix
        mult, mult_common = CHANNELS[common]
        return multiplexers[mult].get_mux(mult_common)

    def get_mults(self):
        return multiplexers

    def close(self):
        self.i2c.close()

