import RPi.GPIO as GPIO
import time, os

def setup(robot_config):
    global pl, pr, pp, pc, pitch_enable, claw_enable, sounds

    ds = 'directservo'

    music_file = robot_config.get(ds, 'music_file')
    sounds = []

    if len(music_file):
        with open(music_file, 'r') as f:
            tmp = f.read()
        lines = tmp.split('\n')

        for line in lines:
            splt = line.split(':')
            if len(splt) == 2:
                sounds.append((splt[0], splt[1].strip()))
        print(sounds)

    claw_enable = robot_config.getint(ds, 'claw_enable')
    pitch_enable = robot_config.getint(ds, 'pitch_enable')

    pin_left = robot_config.getint(ds, 'left') # left servo pin
    pin_right = robot_config.getint(ds, 'right') # right servo pin
    
    if claw_enable: pin_pitch = robot_config.getint(ds, 'pitch') # camera pitch servo pin
    
    if pitch_enable: pin_claw = robot_config.getint(ds, 'claw') # claw servo pin

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(pin_left, GPIO.OUT)
    GPIO.setup(pin_right, GPIO.OUT)

    pl = GPIO.PWM(pin_left, 50)
    pr = GPIO.PWM(pin_right, 50)

    pl.start(0)
    pr.start(0)

    if pitch_enable:
        GPIO.setup(pin_pitch, GPIO.OUT)
        pp = GPIO.PWM(pin_pitch, 50)
        pp.start(0)

    if claw_enable:
        GPIO.setup(pin_claw, GPIO.OUT)
        pc = GPIO.PWM(pin_claw, 50)
        pc.start(0)

def check_sounds(command):
    for sound in sounds:
        if sound[0] == command:
            os.system("mplayer {} -softvol -volume 100".format(sound[1]))
            break

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
    global tilt_servo, pitch_enable, claw_enable

    command = args['command']
    if command == 'F':
        servo_set(pl, 15)
        servo_set(pr, 0.1)
    elif command == 'B':
        servo_set(pl, 0.1)
        servo_set(pr, 15)
    elif command == 'R':
        servo_set(pl, 15)
        servo_set(pr, 15)
        time.sleep(t_delay)
        servo_set(pl, 0)
        servo_set(pr, 0)
    elif command == 'L':
        servo_set(pl, 0.1)
        servo_set(pr, 0.1)
        time.sleep(t_delay)
        servo_set(pl, 0)
        servo_set(pr, 0)
    elif command == 'U' and pitch_enable:
        tilt_servo = min(12, tilt_servo + pitch_incr)
        servo_set_time(pp, tilt_servo, 0.1)
    elif command == 'D' and pitch_enable:
        tilt_servo = max(3, tilt_servo - pitch_incr)
        servo_set_time(pp, tilt_servo, 0.5)
    elif command == 'O' and claw_enable:
        servo_set_time(pc, 1, 0.25)
    elif command == 'C' and claw_enable:
        servo_set_time(pc, 15, 0.25)
    else:
        servo_set(pl, 0)
        servo_set(pr, 0)
        if pitch_enable: servo_set(pp, 0)
        if claw_enable: servo_set(pc, 0)

        check_sounds(command)