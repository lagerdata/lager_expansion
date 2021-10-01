from ft260 import FT260
from pca9685 import PCA9685, OutputModes

ADDR = 0x40

class LagerPWM:
    def __init__(self):
        self.dev = FT260()
        self.pca = PCA9685(self.dev, ADDR)
        self.pca.begin()

    def __getattr__(self, func):
        def method(*args):
            method = getattr(self.pca, func)
            method(*args)
        return method

    def close(self):
        self.dev.close()