# Frequency measurement example using PWMCounter.
# It measures frequency generated on GP0
# with counter configured on GP15.

from machine import Pin, PWM
from time import ticks_ms, ticks_diff
from PWMCounter import PWMCounter

# Set PWM to output test signal
pwm = PWM(Pin(0))
pwm.duty_u16(1 << 15)
pwm.freq(1000)

# Configure counter to count rising edges on GP15
counter = PWMCounter(15, PWMCounter.EDGE_RISING)
# Set divisor to 1 (just in case)
counter.set_div()
# Start counter
counter.start()

# Set sampling time in ms
sampling_time = 1000
last_check = ticks_ms()

while True:
    if ticks_diff(tmp := ticks_ms(), last_check) >= sampling_time:
        # Print calculated frequency in Hz - should show 1000 with default setup
        print(counter.read_and_reset() / (sampling_time / 1000))
        last_check = tmp
