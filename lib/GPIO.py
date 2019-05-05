from gpiozero import LED
from lib.guess_device import guess_device

ALERT_LED = None
ERROR_LED = None
OK_LED = None

class GPIO:
    '''
        GPIO Controller

        GPIO indication types:
            OK - Solid green

    '''

    @staticmethod
    def warning():
        GPIO.turn_off_all_led()
        GPIO.blink_alert_led(on_time=0.5, off_time=0.5)

    @staticmethod
    def connecting():
        GPIO.turn_off_all_led()
        GPIO.blink_ok_led(on_time=0.1, off_time=0.1)

    @staticmethod
    def OK():
        GPIO.turn_off_all_led()
        GPIO.turn_ok_led()

    @staticmethod
    def created():
        GPIO.turn_off_all_led()
        GPIO.blink_ok_led(on_time=0.5, off_time=0.5)
    
    @staticmethod
    def error():
        GPIO.turn_off_all_led()
        GPIO.turn_error_led()

    @staticmethod
    def writing():
        GPIO.turn_off_all_led()
        GPIO.turn_ok_led()
        GPIO.blink_alert_led(on_time=0.2, off_time=0.2)
    
    @staticmethod
    def is_gpio_active():
        return guess_device() == "rpi"

    @staticmethod
    def setup_leds():
        global ALERT_LED
        global ERROR_LED
        global OK_LED

        if GPIO.is_gpio_active():
            ALERT_LED = LED(14)
            ERROR_LED = LED(15)
            OK_LED = LED(18)
        else:
            ALERT_LED = None
            ERROR_LED = None
            OK_LED = None

    @staticmethod
    def turn_alert_led(on=True):
        if GPIO.is_gpio_active():
            if on:
                ALERT_LED.on()
            else:
                ALERT_LED.off()

    @staticmethod
    def turn_error_led(on=True):
        if GPIO.is_gpio_active():
            if on:
                ERROR_LED.on()
            else:
                ERROR_LED.off()

    @staticmethod
    def turn_ok_led(on=True):
        if GPIO.is_gpio_active():        
            if on:
                OK_LED.on()
            else:
                OK_LED.off()

    @staticmethod    
    def turn_off_all_led():
        if GPIO.is_gpio_active():
            OK_LED.off()
            ERROR_LED.off()
            ALERT_LED.off()

    @staticmethod
    def blink_alert_led(on_time=1, off_time=1, count=None):
        if GPIO.is_gpio_active():
            if count:
                ALERT_LED.blink(on_time=on_time, off_time=off_time, n=count)
            else:
                ALERT_LED.blink(on_time=on_time, off_time=off_time)

    @staticmethod
    def blink_ok_led(on_time=1, off_time=1, count=None):
        if GPIO.is_gpio_active():
            if count:
                OK_LED.blink(on_time=on_time, off_time=off_time, n=count)
            else:
                OK_LED.blink(on_time=on_time, off_time=off_time)

    @staticmethod
    def blink_error_led(on_time=1, off_time=1, count=None):
        if GPIO.is_gpio_active():
            if count:
                ERROR_LED.blink(on_time=on_time, off_time=off_time, n=count)
            else:
                ERROR_LED.blink(on_time=on_time, off_time=off_time)
