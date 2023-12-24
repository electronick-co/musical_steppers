from machine import Pin, Timer
import utime
import uselect, sys

dir1_pin = Pin(16, Pin.OUT)
step1_pin = Pin(17, Pin.OUT)
dir2_pin = Pin(18, Pin.OUT)
step2_pin = Pin(19, Pin.OUT)

steps_per_revolution = 200

# Initialize timer

tim1 = Timer()
tim2 = Timer()

#Notes

notes = [1912,1703,1517,1431,1275,1136,1012]


c = 1912
cf = 1805
d = 1703
df = 1607
e = 1517
f = 1431
ff = 1351
g = 1275
gf = 1203
a = 1136
af = 1072
b = 1012

  

delay_flag = 0

def step1(t):
    global step1_pin
    global delay_flag

    step1_pin.value(not step1_pin.value())
    if delay_flag:

        step2_pin.value(not step2_pin.value())
        delay_flag = 0
    else:
        delay_flag = 1

  

def step2(t):
    global step2_pin
    step2_pin.value(not step2_pin.value())

def rotate_motor1(delay):
    # Set up timer for stepping
    tim1.init(freq=1000000//delay, mode=Timer.PERIODIC, callback=step1)

  

def rotate_motor2(delay):

    # Set up timer for stepping
    tim2.init(freq=1000000//delay, mode=Timer.PERIODIC, callback=step2)
    spoll=uselect.poll()
    spoll.register(sys.stdin,uselect.POLLIN)

# def read1():
#     return(sys.stdin.read(1) if spoll.poll(0) else None)

def loop():

    dir1_pin.value(1)

    while True:
    # c = read1()
    # if c:
    # print(f"letter {c}")
    # # Spin motor slowly
    # if int(c)-1 >= 0 and int(c)-1 < 7:
    # rotate_motor1(notes[int(c)-1])
    # rotate_motor2(notes[int(c)-1]*2)
    # # utime.sleep_ms(steps_per_revolution)

        for n in notes:
            # Set motor direction clockwise
            dir1_pin.value(not dir1_pin.value())
            dir2_pin.value(not dir2_pin.value())
            # Spin motor slowly
            rotate_motor1(n)
            utime.sleep_ms(steps_per_revolution)
            tim1.deinit() # stop the timer
        utime.sleep(1)

    # # Set motor direction counterclockwise

    # dir1_pin.value(0)

    # # Spin motor quickly

    # rotate_motor(1000)

    # utime.sleep_ms(steps_per_revolution)

    # tim.deinit() # stop the timer

    # utime.sleep(1)

if __name__ == '__main__':
    print("begins now!")
    loop()