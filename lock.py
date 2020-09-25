import RPi.GPIO as GPIO
import time

channel = 7
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)

def lock_on(pin):
    GPIO.output(pin, GPIO.HIGH)

def lock_off(pin):
    GPIO.output(pin, GPIO.LOW)

try:
    lock_on(channel)
    time.sleep(2)
    lock_off(channel)
    time.sleep(1)
    GPIO.cleanup()
    print("LOCK OPENED...")
except KeyboardInterrupt:
    GPIO.cleanup()
