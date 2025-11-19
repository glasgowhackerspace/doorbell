import time
import pigpio

SERVO_PIN = 4

def main():
    pwm = pigpio.pi()
    pwm.set_mode(SERVO_PIN, pigpio.OUTPUT)
    pwm.set_PWM_frequency(SERVO_PIN, 50)

    pwm.set_servo_pulsewidth(SERVO_PIN, 500)
    time.sleep(0.3)
    pwm.set_servo_pulsewidth(SERVO_PIN, 2500)
    time.sleep(0.5)

    pwm.set_PWM_dutycycle(SERVO_PIN, 0)
    pwm.set_PWM_frequency(SERVO_PIN, 0)


if __name__ == "__main__":
    main()

