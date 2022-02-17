from .ft260 import FT260
from .max14661 import MAX14661

ADDRS = [0x4c, 0x4d, 0x4e, 0x4f]
multiplexers = []
CHANNELS = {'A': (0, 'A'), 'B': (0, 'B'), 'C': (1, 'A'), 'D': (1, 'B'), 'E': (2, 'A'), 'F': (2, 'B'), 'G': (3, 'A'), 'H': (3, 'B')}
MULT_MAP_INPUTS = [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, -1]

class LagerMultiplexer:
    def __init__(self):
        self.i2c = FT260(debug=False)
        
        for addr in ADDRS:
            multiplexers.append(MAX14661(self.i2c, addr))

    def validate_mux(self, inp, out):
        inp = int(inp)
        if inp < 0 or inp > 15:
            raise ValueError

        if out.upper() not in CHANNELS.keys():
            raise ValueError

        return inp, out

    def mux(self, common, channel):
        mult, mult_common = CHANNELS[common]
        print(f"Muxing input {channel} to output {common}")
        channel = MULT_MAP_INPUTS[channel]
        # print(f"\tActually mult {mult}, input {channel} output {mult_common}")
        multiplexers[mult].mux(mult_common, channel)

    def get_mux(self, common):
        # TODO fix
        mult, mult_common = CHANNELS[common]
        return multiplexers[mult].get_mux(mult_common)

    def get_mults(self):
        return multiplexers

    def clear_mux(self, mux):
        multiplexers[mux].clear()

    def clear_all(self):
        for mux in multiplexers:
            mux.clear()

    def close(self):
        self.i2c.close()

