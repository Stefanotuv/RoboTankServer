from time import sleep
from machine import Pin, PWM
import machine
import time, utime

pwm_freq = 1500
SPEED = 1

# Pin Definitions
motor_a_pwm_pin = machine.Pin(6)  # GP18 as PWM pin for motor speed control
motor_a_in1_pin = machine.Pin(7, Pin.OUT)  # GP19 as IN1 pin for motor direction control
motor_a_in2_pin = machine.Pin(8, Pin.OUT)  # GP20 as IN2 pin for motor direction control
motor_a_pwm = machine.PWM(motor_a_pwm_pin)
motor_a_pwm.freq(1500)

motor_b_pwm_pin = machine.Pin(10)  # GP18 as PWM pin for motor speed control
motor_b_in1_pin = machine.Pin(11, Pin.OUT)  # GP19 as IN1 pin for motor direction control
motor_b_in2_pin = machine.Pin(12, Pin.OUT)  # GP20 as IN2 pin for motor direction control
motor_b_pwm = machine.PWM(motor_b_pwm_pin)
motor_b_pwm.freq(1500)


# Set the PWM frequency to 1500Hz (adjust this value as needed)


class Motor_Speed_Main:
    def __init__(self, motor_a_in1_pin=motor_a_in1_pin, motor_a_in2_pin=motor_a_in2_pin,
                 motor_b_in1_pin=motor_b_in1_pin, motor_b_in2_pin=motor_b_in2_pin):
        self.a_forward = motor_a_in1_pin
        self.a_back = motor_a_in2_pin
        self.b_forward = motor_b_in1_pin
        self.b_back = motor_b_in2_pin
        # Initialize PWM objects for motor control
        self.motor_a_pwm = motor_a_pwm
        self.motor_b_pwm = motor_b_pwm
        pass

    # Set the speed to 50% (you can change this value as needed) range 1 - 0.6 (.5 doesnt move)
    def move_forward(self, speed=SPEED):
        print("Moving Backward")

        self.a_forward.value(0)
        self.b_forward.value(0)
        self.a_back.value(1)
        self.b_back.value(1)

        self.motor_a_pwm.duty_u16(int(speed * 65535))
        self.motor_b_pwm.duty_u16(int(speed * 65535))
        sleep(.5)
        self.move_stop()

    def move_backward(self, speed=SPEED):
        print("Moving Forward")

        self.a_forward.value(1)
        self.b_forward.value(1)
        self.a_back.value(0)
        self.b_back.value(0)

        self.motor_a_pwm.duty_u16(int(speed * 65535))
        self.motor_b_pwm.duty_u16(int(speed * 65535))

        sleep(.5)
        self.move_stop()

    def move_left(self, speed=SPEED):
        print("Moving Left")
        self.a_forward.value(1)
        self.b_forward.value(0)
        self.a_back.value(0)
        self.b_back.value(1)

        self.motor_a_pwm.duty_u16(int(speed * 65535))
        self.motor_b_pwm.duty_u16(int(speed * 65535))

        sleep(.5)
        self.move_stop()

    def move_right(self, speed=SPEED):
        print("Moving Rigt")
        self.a_forward.value(0)
        self.b_forward.value(1)
        self.a_back.value(1)
        self.b_back.value(0)

        self.motor_a_pwm.duty_u16(int(speed * 65535))
        self.motor_b_pwm.duty_u16(int(speed * 65535))
        sleep(.5)
        self.move_stop()

    def move_backward_continue(self, speed=SPEED):
        print("Moving Backward")

        self.a_forward.value(0)
        self.b_forward.value(0)
        self.a_back.value(1)
        self.b_back.value(1)
        print("speed move_backward_continue:")
        print(speed)
        self.motor_a_pwm.duty_u16(int(speed * 65535))
        self.motor_b_pwm.duty_u16(int(speed * 65535))

    def move_forward_continue(self, speed=SPEED):
        print("Moving Forward")

        self.a_forward.value(1)
        self.b_forward.value(1)
        self.a_back.value(0)
        self.b_back.value(0)
        print("speed move_forward_continue:")
        print(speed)
        print(f'speed move_forward_continue:{int(speed * 65535)}')

        self.motor_a_pwm.duty_u16(int(speed * 65535))
        self.motor_b_pwm.duty_u16(int(speed * 65535))

    def move_left_continue(self, speed=SPEED):
        print("Moving Left")
        self.a_forward.value(1)
        self.b_forward.value(0)
        self.a_back.value(0)
        self.b_back.value(1)
        print("speed move_left_continue:")
        print(speed)
        self.motor_a_pwm.duty_u16(int(speed * 65535))
        self.motor_b_pwm.duty_u16(int(speed * 65535))

    def move_right_continue(self, speed=SPEED):
        print("Moving Rigt")
        self.a_forward.value(0)
        self.b_forward.value(1)
        self.a_back.value(1)
        self.b_back.value(0)
        print("speed move_right_continue:")
        print(speed)
        self.motor_a_pwm.duty_u16(int(speed * 65535))
        self.motor_b_pwm.duty_u16(int(speed * 65535))

    def move_stop(self):
        self.a_forward.value(0)
        self.b_forward.value(0)
        self.a_back.value(0)
        self.b_back.value(0)
