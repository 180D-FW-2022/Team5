import smbus2

class Sensor:
    def __init__(self, device_address, XL, XH, YL, YH, ZL, ZH):
        self.bus = smbus2.SMBus(1)
        self.device_address = device_address
        self.XL = XL
        self.XH = XH
        self.YL = YL
        self.YH = YH
        self.ZL = ZL
        self.ZH = ZH

    def writeByte(self, register, value):
        self.bus.write_byte_data(self.device_address, register, value)

    # Read 2-byte value with L bit stored in add_l and H bit stored in add2_h
    def read16BitValue(self, add_l, add_h):
        byte_l = self.bus.read_byte_data(self.device_address, add_l)
        byte_h = self.bus.read_byte_data(self.device_address, add_h)

        combined = (byte_l | byte_h <<8)
        return combined  if combined < 32768 else combined - 65536

    def readRaw(self):
        x = self.read16BitValue(self.XL, self.XH)
        y = self.read16BitValue(self.YL, self.YH)
        z = self.read16BitValue(self.ZL, self.ZH)

        return x, y, z
