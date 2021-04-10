# Pulse width measurement example using PWMCounter.
#
# Measures pulse width of PWM generated on GP0
# with counter configured on GP15.

from machine import Pin, PWM
from time import ticks_us, ticks_diff
from PWMCounter import PWMCounter

# Set PWM to output test signal
pwm = PWM(Pin(0))
# Set duty cycle to 25%
pwm.duty_u16(1 << 14)
pwm.freq(1000)

# We'll use counter pin for triggering, so set it up.
in_pin = Pin(15, Pin.IN)
# Configure counter to count rising edges on GP15
counter = PWMCounter(15, PWMCounter.LEVEL_HIGH)
# Set divisor to 16 (helps avoid counter overflow)
counter.set_div(16)
# Start counter
counter.start()

last_state = 0
last_update = ticks_us()
while True:
    start = ticks_us()
    if ~(x := in_pin.value()) & last_state:
        # Print pulse width in us - should show 250 with default setup
        print((counter.read_and_reset() * 16) / 125)
    last_state = x
