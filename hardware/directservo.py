from RPIO import PWM
import time

def setup(robot_config):
    global servos, pitch_enable, claw_enable
    global pin_left, pin_right, pin_pitch, pin_claw

    ds = 'directservo'

    claw_enable = robot_config.getint(ds, 'claw_enable')
    pitch_enable = robot_config.getint(ds, 'pitch_enable')

    pin_left = robot_config.getint(ds, 'left') # left servo pin
    pin_right = robot_config.getint(ds, 'right') # right servo pin
    
    servos = PWM.Servo()

    if claw_enable:
        pin_pitch = robot_config.getint(ds, 'pitch') # camera pitch servo pin
    else:
        pin_pitch = -1

    if pitch_enable:
        pin_claw = robot_config.getint(ds, 'claw') # claw servo pin
    else:
        pin_claw = -1


def servo_set(servo, value):
    servos.set_servo(servo, value)

def servo_set_time(servo, value, t):
    servo_set(servo, value)
    time.sleep(t)
    servo_set(servo, 0)

tilt_servo = 6 # roughly middle for 50ms pwm range
pitch_incr = 0.2 # increment 
t_delay = 0.06
def move(args):
    global tilt_servo, pitch_enable, claw_enable
    global pin_left, pin_right, pin_pitch, pin_claw

    command = args['command']
    
    if command == 'F':
        servo_set(pin_left, 15)
        servo_set(pin_right, 1)
    elif command == 'B':
        servo_set(pin_left, 1)
        servo_set(pin_right, 15)

    elif command == 'R':
        servo_set(pin_left, 15)
        servo_set(pin_right, 15)
        time.sleep(t_delay)
        servo_set(pin_left, 0)
        servo_set(pin_right, 0)
    elif command == 'L':
        servo_set(pin_left, 1)
        servo_set(pin_right, 1)
        time.sleep(t_delay)
        servo_set(pin_left, 0)
        servo_set(pin_right, 0)

    elif command == 'U' and pitch_enable:
        tilt_servo = min(12, tilt_servo + pitch_incr)
        servo_set_time(pin_pitch, tilt_servo, 0.1)
    elif command == 'D' and pitch_enable:
        tilt_servo = max(3, tilt_servo - pitch_incr)
        servo_set_time(pin_pitch, tilt_servo, 0.5)

    elif command == 'O' and claw_enable:
        servo_set_time(claw_enable, 1, 0.25)
    elif command == 'C' and claw_enable:
        servo_set_time(claw_enable, 15, 0.25)

    else:
        servo_set(pin_left, 0)
        servo_set(pin_right, 0)
        if pitch_enable: servo_set(pin_pitch, 0)
        if claw_enable: servo_set(claw_enable, 0)