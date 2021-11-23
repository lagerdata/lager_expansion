from .ft260 import Flags

# registers
MAX14661_DIR0       = 0x00
MAX14661_DIR1       = 0x01
MAX14661_DIR2       = 0x02
MAX14661_DIR3       = 0x03
MAX14661_SHDW0      = 0x10
MAX14661_SHDW1      = 0x11
MAX14661_SHDW2      = 0x12
MAX14661_SHDW3      = 0x13
MAX14661_CMD_A      = 0x14
MAX14661_CMD_B      = 0x15

class MAX14661:
    def __init__(self, i2c, address):
        self.i2c = i2c
        self.address = address

    def begin(self):
        pass

    def mux_a(self, channel):
        if channel <= 0 or channel > 15:
            channel = 0x10 # Disable all switches
        else:
            channel -= 1
        
        print(f"Writing to {hex(self.address)} {hex(MAX14661_CMD_A)} {hex(channel)}")
        self.i2c.write(self.address, Flags.FLAG_START_STOP, [MAX14661_CMD_A, channel, 0x10])

    def mux_b(self, channel):
        if channel <= 0 or channel > 15:
            channel = 0x10 # Disable all switches
        else:
            channel -= 1
        # print(f"Writing to {hex(self.address)} {hex(MAX14661_CMD_B)} {hex(channel)}")
        self.i2c.write(self.address, Flags.FLAG_START_STOP, [MAX14661_CMD_A, 0x10, channel])

    def mux(self, common, channel):
        if common == 'A':
            self.mux_a(channel)
        elif common == 'B':
            self.mux_b(channel)

    def get_mux_a(self):
        mux_a = self.i2c.read(self.address, MAX14661_CMD_A, 1)
        return mux_a

    def get_mux_b(self):
        mux_b = self.i2c.read(self.address, MAX14661_CMD_B, 1)
        return  mux_b

    def get_mux(self, common):
        if common == 'A':
            return self.get_mux_a()
        elif common == 'B':
            return self.get_mux_b()

    def test(self):

        # self.i2c.write(self.address, Flags.FLAG_START_STOP, [MAX14661_DIR0, 0x02])

        dir0 = self.i2c.read(self.address, MAX14661_DIR0, 1)
        dir1 = self.i2c.read(self.address, MAX14661_DIR1, 1)
        dir2 = self.i2c.read(self.address, MAX14661_DIR2, 1)
        dir3 = self.i2c.read(self.address, MAX14661_DIR3, 1)
        print(f"DIR0: {hex(dir0[0])} DIR1: {hex(dir1[0])} DIR2: {hex(dir2[0])} DIR3: {hex(dir3[0])}")