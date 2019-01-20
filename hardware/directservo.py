import RPi.GPIO as GPIO
import time

def setup(robot_config):
    global pl, pr, pp, pc

    ds = 'directservo'
    pin_left = robot_config.getint(ds, 'left') # left servo pin
    pin_right = robot_config.getint(ds, 'right') # right servo pin
    pin_pitch = robot_config.getint(ds, 'pitch') # camera pitch servo pin
    pin_claw = robot_config.getint(ds, 'claw') # claw servo pin

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(pin_left, GPIO.OUT)
    GPIO.setup(pin_right, GPIO.OUT)
    GPIO.setup(pin_pitch, GPIO.OUT)
    GPIO.setup(pin_claw, GPIO.OUT)

    pl = GPIO.PWM(pin_left, 50)
    pr = GPIO.PWM(pin_right, 50)
    pp = GPIO.PWM(pin_pitch, 50)
    pc = GPIO.PWM(pin_claw, 50)

    pl.start(0)
    pr.start(0)
    pp.start(0)
    pc.start(0)

def servo_set(servo, value):
    servo.ChangeDutyCycle(value)

def servo_set_time(servo, value, t):
    servo_set(servo, value)
    time.sleep(t)
    servo_set(servo, 0)

tilt_servo = 6 # roughly middle for 50ms pwm range
pitch_incr = 0.2 # increment 
t_delay = 0.06
def move(args):
    global tilt_servo

    command = args['command']
    if command == 'F':
        servo_set(pl, 15)
        servo_set(pr, 1)
    elif command == 'B':
        servo_set(pl, 1)
        servo_set(pr, 15)
    elif command == 'R':
        servo_set(pl, 15)
        servo_set(pr, 15)
        time.sleep(t_delay)
        servo_set(pl, 0)
        servo_set(pr, 0)
    elif command == 'L':
        servo_set(pl, 1)
        servo_set(pr, 1)
        time.sleep(t_delay)
        servo_set(pl, 0)
        servo_set(pr, 0)
    elif command == 'U':
        tilt_servo = min(12, tilt_servo + pitch_incr)
        servo_set_time(pp, tilt_servo, 0.1)
    elif command == 'D':
        tilt_servo = max(3, tilt_servo - pitch_incr)
        servo_set_time(pp, tilt_servo, 0.5)
    elif command == 'O':
        servo_set_time(pc, 1, 0.25)
    elif command == 'C':
        servo_set_time(pc, 15, 0.25)
    else:
        servo_set(pl, 0)
        servo_set(pr, 0)
        servo_set(pp, 0)
        servo_set(pc, 0)