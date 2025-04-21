from machine import mem32
from os import uname


MCU_RP2040 = 0
MCU_RP235X = 1

if 'RP2040' in uname()[4]:
    IO_BANK0_BASE = 0x40014000
    PWM_BASE = 0x40050000
    MAX_PINS = 30
    MCU = MCU_RP2040
elif 'RP235' in uname()[4]:
    IO_BANK0_BASE = 0x40028000
    PWM_BASE = 0x400a8000
    MAX_PINS = 48
    MCU = MCU_RP235X
else:
    raise OSError('Unsupported MCU.')


class PWMCounter:
    LEVEL_HIGH = 1
    EDGE_RISING = 2
    EDGE_FALLING = 3

    def __init__(self, pin, condition=LEVEL_HIGH):
        assert pin < MAX_PINS and pin % 2, "Invalid pin number"
        slice_offset = pin // 2 % 8 * 20 if pin < 32 else (pin // 2 % 4 + 8) * 20
        self._csr = PWM_BASE | (0x00 + slice_offset)
        self._ctr = PWM_BASE | (0x08 + slice_offset)
        self._div = PWM_BASE | (0x04 + slice_offset)
        self._condition = condition
        self.setup(pin)

    def setup(self, pin):
        # Set pin to PWM
        mem32[IO_BANK0_BASE | (0x04 + pin * 8)] = 4
        # If using RP235x clear pad isolation and set input enable.
        if MCU == MCU_RP235X:
            mem32[0x40039004 + 0x04 * pin] = 0x140
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

    def set_div(self, int_=1, frac=0):
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
