___
# PWMCounter
-------------
This module aims to simplify using PWM hardware in edge- and level-sensitive modes.

Full description can be found in [RP2040 datasheet](https://datasheets.raspberrypi.org/rp2040/rp2040-datasheet.pdf)
and [RP2350 datasheet](https://datasheets.raspberrypi.com/rp2350/rp2350-datasheet.pdf).

---
# Pin selection
Pico hardware allows only odd-numbered GPIOs to be used in counter mode. 
Some pins share the same PWM slice (see list below) and if they are used in counting mode at the same time the signal seen by counter is a logical OR of both inputs.

| PWM slice   | GPIOs |
| :---------: | :-----:|
| 0           | GP1, GP17 |
| 1           | GP3, GP19 |
| 2           | GP5, GP21 |
| 3           | GP7, GP23 |
| 4           | GP9, GP25 |
| 5           | GP11, GP27 |
| 6           | GP13, GP29 |
| 7           | GP15 |

Additionally, on RP235X:

| PWM slice   | GPIOs |
| :---------: | :-----:|
| 7           | GP31 |
| 8           | GP33, GP41 |
| 9           | GP35, GP43 |
| 10          | GP37, GP45 |
| 11          | GP39, GP47 |

NOTE! GPIOs above GP30 are only available in the QFN-80 package, i.e. RP2350**B** and RP2354**B**.

---
# Clock divider
(excerpt from datasheet)

This  is  an  8  integer  bit,  4  fractional  bit  clock divider, which allows the count rate to be slowed by up to a factor of 256.

The  clock  divider  also  allows  the  effective  count  range  to  be  extended  when  using  level-sensitive  or  edge-sensitive modes to take duty cycle or frequency measurements.
___
# Methods

___
## __init__(pin, mode)

Sets up **pin** to be used as a counter in the selected **mode**.

**pin** - GP number to use (not Pin object).

**mode** - can be one of the following:

1. LEVEL_HIGH - counter increments only when input is high. Can be used to measure pulse width or duty cycle. (default value)
2. EDGE_RISING - counter increments on rising input edge. Can be used to measure frequency.
3. EDGE_FALLING - counter increments on falling input edge. Can be used to measure frequency.

----

## start()

Starts counter operation.

----

## stop()

Stops counter operation. Retains the current count.

---

## reset()

Resets counter to 0.

---

## read()

Returns the current counter value.

---

## read_and_reset()

Combines __read()__ and __reset()__ methods.

---

## set\_div(int\_, frac)

Allows setting a fractional clock divider. If called without parameters, sets divider to 1.

__int\___ - integer part of the divder. (defaults to 1)

__frac__ - fractional part of the divider. (defaults to 0)

---

# Example
This example generates 100 short pulses on GP0 and counts them using PWMCounter configured on GP15.

```python
from machine import Pin
from PWMCounter import PWMCounter

output = Pin(0, Pin.OUT)

counter = PWMCounter(15, PWMCounter.EDGE_RISING)
counter.set_div()
counter.start()

for i in range(100):
    output.value(1)
    output.value(0)

print("Pulses expected: 100")
print("Pulses detected: {}".format(counter.read()))
```
