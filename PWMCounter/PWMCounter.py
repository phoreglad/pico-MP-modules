from machine import mem32

_conditions = {"FREE" : 0x0, "GATED" : 0x1, "EDGE_RISING" : 0x2, "EDGE_FALLING" : 0x3}

class PWMCounter:
    def __init__(self, pin, condition = "FREE"):
        assert pin < 30
        # Only odd pins can be counter inputs
        assert pin % 2
        self.pin_reg = 0x40014000 | (0x04 + pin * 8)
        self.csr = 0x40050000 | (0x00 + (pin % 16) // 2 * 20)
        self.ctr = 0x40050000 | (0x08 + (pin % 16) // 2 * 20)
        self.div = 0x40050000 | (0x04 + (pin % 16) // 2 * 20)
#         print(hex(self.pin_reg), hex(self.csr), hex(self.ctr))
        self.condition = condition
        self.setup()
    
    def setup(self):
        # Set pin to PWM
        mem32[self.pin_reg] = 4
        # Setup PWM counter for selected pin to chosen counter mode
        mem32[self.csr] = _conditions[self.condition] << 4
        self.reset()
    
    def start(self):
        mem32[self.csr + 0x2000] = 1
        
    def stop(self):
        mem32[self.csr + 0x3000] = 1
    
    def reset(self):
        mem32[self.ctr] = 0
    
    def read(self):
        return mem32[self.ctr]
    
    def read_and_reset(self):
        tmp = self.read()
        self.reset()
        return tmp
    
    def set_div(self, div):
        # This function is quite dumb. Use with care.
        mem32[self.div] = div

if __name__ == "__main__":
    from machine import Pin
    output = Pin(2, Pin.OUT)
    counter = PWMCounter(15, "EDGE_RISING")
#     counter._conditions["EDGE_RISING"] = 5
#     print(counter._conditions)
#     counter.start()
#     for i in range(5):
#         output.value(1)
#         output.value(0)
#         print(counter.read())