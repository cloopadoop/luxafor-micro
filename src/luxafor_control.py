import hid

class LuxaforControl:
    def __init__(self):
        self.VENDOR_ID = 0x04d8
        self.PRODUCT_ID = 0xf372
        self.device = None
        self.current_color = None
        self.connect_device()

    def connect_device(self):
        try:
            self.device = hid.device()
            self.device.open(self.VENDOR_ID, self.PRODUCT_ID)
            return True
        except Exception:
            return False

    def write_command(self, command):
        if not self.device and not self.connect_device():
            return False
        try:
            self.device.write(command)
            return True
        except Exception:
            return False

    def set_color(self, r, g, b, led=255):
        self.current_color = [r, g, b]
        return self.write_command([0x00, 0x01, led, r, g, b, 0x00, 0x00, 0x00])

    def turn_off(self):
        self.current_color = [0, 0, 0]
        return self.set_color(0, 0, 0)
