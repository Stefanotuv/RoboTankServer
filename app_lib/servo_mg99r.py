from machine import Pin, PWM
from time import sleep

MID_MG995R = 1500000  # Adjust this value based on MG995R's center position
MIN_MG995R = 800000   # Adjust this value based on MG995R's minimum position
MAX_MG995R = 2200000  # Adjust this value based on MG995R's maximum position
STEP_MG995R = 50000   # Adjust this value based on MG995R's step size

class Servo:
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin, Pin.OUT))
        self.pwm.freq(50)
        self.current_pos = MID_MG995R  # Initialize to MG995R's center
        self.pwm.duty_ns(MID_MG995R)
        self.name = str(pin)

    def right(self, input=20):
        value = self.current_pos - int(STEP_MG995R / input)
        if value > MAX_MG995R:
            value = MAX_MG995R
        self.current_pos = value
        self.pwm.duty_ns(value)
        sleep(0.1)

    def left(self, input=20):
        value = self.current_pos + int(STEP_MG995R / input)
        if value < MIN_MG995R:
            value = MIN_MG995R
        self.current_pos = value
        self.pwm.duty_ns(value)
        sleep(0.1)

    def down(self, input=20):
        value = self.current_pos + int(STEP_MG995R / input)
        if value > MAX_MG995R:
            value = MAX_MG995R
        self.current_pos = value
        self.pwm.duty_ns(value)
        sleep(0.1)

    def up(self, input=20):
        value = self.current_pos - int(STEP_MG995R / input)
        if value < MIN_MG995R:
            value = MIN_MG995R
        self.current_pos = value
        self.pwm.duty_ns(value)
        sleep(0.1)

    def center(self):
        if self.current_pos > MID_MG995R:
            while (self.current_pos - STEP_MG995R) > MID_MG995R:
                self.current_pos -= STEP_MG995R
                self.pwm.duty_ns(self.current_pos)
                sleep(0.3)
            self.current_pos = MID_MG995R
            self.pwm.duty_ns(self.current_pos)
        elif self.current_pos < MID_MG995R:
            while (self.current_pos + STEP_MG995R) < MID_MG995R:
                self.current_pos += STEP_MG995R
                self.pwm.duty_ns(self.current_pos)
                sleep(0.3)
            self.current_pos = MID_MG995R
            self.pwm.duty_ns(self.current_pos)

# Example usage:
# mg995r_servo = Servo(your_pin_number)
# mg995r_servo.center()  # Initialize to the center position
