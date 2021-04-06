from machine import Pin, mem32

class Buttons:
    def __init__(self):
        self.buttons = []
        self._state = 0
        self._delta = 0
        self._cnt0 = 0
        self._cnt1 = 0
        self._toggle = 0
        self._last_state = 0
    
    def add_button(self, Button):
        self.buttons.append(Button)
        # Every time new button is added set _state and _last_state to current
        # input value to avoid false edge detection on start
        self._state = self._last_state = mem32[0xd0000004]
    
    def debounce(self):
        """
        Debounce inputs using vertical counter.
        Source: https://www.compuphase.com/electronics/debouncing.htm
        """
        sample = mem32[0xd0000004]
        self._delta = sample ^ self._state
        self._cnt1 = (self._cnt1 ^ self._cnt0) & self._delta
        self._cnt0 = ~self._cnt0 & self._delta
        self._state ^= (self._cnt0 & self._cnt1)
        return self._state
    
    def check_buttons(self):
        """
        Check button states and run relevant functions.
        To use run this method every couple ms (defines debouncing time).
        """
        current_state = self.debounce()
        rising_edges = current_state & ~self._last_state
        falling_edges = ~current_state & self._last_state
        if falling_edges > 0 or rising_edges > 0:
            for button in self.buttons:
                if rising_edges >> button.pin & 1:
                    button.run_rising()
                if falling_edges >> button.pin & 1:
                    button.run_falling()
        self._last_state = current_state

class Button:
    def __init__(self, pin, pull = Pin.PULL_UP,
                 on_rising = None, on_rising_args = None,
                 on_falling = None, on_falling_args = None):
        Pin(pin, Pin.IN, pull)
        self.pin = pin
        self.on_rising = on_rising
        self.on_rising_args = on_rising_args
        self.on_falling = on_falling
        self.on_falling_args = on_falling_args
    
    def rising_func(self, on_rising, on_rising_args):
        """Define new rising edge function"""
        self.on_rising = on_rising
        self.on_rising_args = on_rising_args
    
    def falling_func(self, on_falling, on_falling_args):
        """Define new falling edge function"""
        self.on_falling = on_falling
        self.on_falling_args = on_falling_args
    
    def run_rising(self):
        if self.on_rising is not None:
            if self.on_rising_args is not None:
                return self.on_rising(self.pin, *self.on_rising_args)
            else:            
                return self.on_rising(self.pin)
    
    def run_falling(self):
        if self.on_falling is not None:
            if self.on_falling_args is not None:
                return self.on_falling(self.pin, *self.on_falling_args)
            else:            
                return self.on_falling(self.pin)

if __name__ == "__main__":
    from time import ticks_ms, ticks_diff
    
    led = Pin(25, Pin.OUT, Pin.PULL_DOWN)
    
    def led_on(p):
        led.value(1)
        print("LED ON")
        
    def led_off(p):
        led.value(0)
        print("LED OFF")
    
    def argtest(p, a1):
        print(a1)
    
    btns = Buttons()
    btns.add_button(Button(4, on_falling = led_on,
                          on_rising = led_off))
    btns.add_button(Button(5, on_rising = led_on))
    btns.add_button(Button(6, on_falling = led_off))
    # args have to be a tuple! Even if there's only one.
    btns.add_button(Button(7, on_falling = argtest, on_falling_args = ("Hello",),
                          on_rising = argtest, on_rising_args = ("World!",)))
    
    print("Ready!\n")
    last_time = ticks_ms()
    while True:
        # Running check_buttons every 10 ms gives around 40 ms debounce period.
        # Should be ok for most switches.
        if ticks_diff(ticks_ms(), last_time) > 10:
            btns.check_buttons()
            last_time = ticks_ms()
