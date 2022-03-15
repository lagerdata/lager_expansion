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
        self.mux_states = [0, 0]

    def begin(self):
        pass

    def mux(self, common, channel):
        if channel <= 0 or channel > 16:
            raise AttributeError("Channel must be between 1-16")
        
        if common == 'A':
            other_reg = 0x10 if self.mux_states[1] == 0 else self.mux_states[1] - 1
            cmd = [MAX14661_CMD_A, channel - 1, other_reg]
            self.mux_states[0] = channel
        
        elif common == 'B':
            other_reg = 0x10 if self.mux_states[0] == 0 else self.mux_states[0] - 1
            cmd = [MAX14661_CMD_A, other_reg, channel - 1]
            self.mux_states[1] = channel

        self.i2c.write(self.address, Flags.FLAG_START_STOP, cmd)

    def clear(self, common):
        if common == 'A':
            other_reg = 0x10 if self.mux_states[1] == 0 else self.mux_states[1] - 1
            cmd = [MAX14661_CMD_A, 0x10, other_reg]
            self.mux_states[0] = 0
        
        elif common == 'B':
            other_reg = 0x10 if self.mux_states[0] == 0 else self.mux_states[0] - 1
            cmd = [MAX14661_CMD_A, other_reg, 0x10]
            self.mux_states[1] = 0

        self.i2c.write(self.address, Flags.FLAG_START_STOP, cmd)

    def get_state(self, common):
        if common == 'A':
            return self.mux_states[0]
        elif common == 'B':
            return self.mux_states[1]
        raise AttributeError("Common must be A or B")
                