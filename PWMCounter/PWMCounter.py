from machine import mem32

class PWMCounter:
    LEVEL_HIGH = 1
    EDGE_RISING = 2
    EDGE_FALLING = 3
    
    def __init__(self, pin, condition = LEVEL_HIGH):
        assert pin < 30 and pin % 2, "Invalid pin number"
        slice_offset = (pin % 16) // 2 * 20
        self._pin_reg = 0x40014000 | (0x04 + pin * 8)
        self._csr = 0x40050000 | (0x00 + slice_offset)
        self._ctr = 0x40050000 | (0x08 + slice_offset)
        self._div = 0x40050000 | (0x04 + slice_offset)
        self._condition = condition
        self.setup()
    
    def setup(self):
        # Set pin to PWM
        mem32[self._pin_reg] = 4
        # Setup PWM counter for selected pin to chosen counter mode
        mem32[self._csr] = self._condition << 4
        self.reset()
    
    def start(self):
        mem32[self._csr + 0x2000] = 1
        
    def stop(self):
        mem32[self._csr + 0x3000] = 1
    
    def reset(self):
        mem32[self._ctr] = 0
    
    def read(self):
        return mem32[self._ctr]
    
    def read_and_reset(self):
        tmp = self.read()
        self.reset()
        return tmp
    
    def set_div(self, int_ = 1, frac = 0):
        if int_ == 256: int_ = 0
        mem32[self._div] = (int_ & 0xff) << 4 | frac & 0xf

if __name__ == "__main__":
    from machine import Pin
    output = Pin(2, Pin.OUT)
    counter = PWMCounter(15, PWMCounter.EDGE_RISING)
    counter.start()
    for i in range(5):
        output.value(1)
        output.value(0)
        print(counter.read())
