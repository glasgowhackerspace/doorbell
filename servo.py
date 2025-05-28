import RPi.GPIO as gpio
from time import sleep

SERVO_PIN = 11
pwm = None

def setAngle(angle):
    duty = angle / 18 + 2.5
    pwm.ChangeDutyCycle(duty)
    sleep(0.3)

def main():
    global pwm
    gpio.setmode(gpio.BOARD)
    gpio.setup(SERVO_PIN, gpio.OUT)
    pwm = gpio.PWM(SERVO_PIN, 50)
    pwm.start(0)

    setAngle(0)
    setAngle(179)

if __name__ == "__main__":
    try:
        main()
    finally:
        print("\nRunning cleanup\n")
        if pwm:
            pwm.stop()
        gpio.cleanup()


