import json
import os

from time import sleep

import lib.templates as templates
from lib.GPIO import GPIO
from lib.setup import setup
from lib.ws import WS

ROOT_DIR = os.getcwd()

if __name__ == "__main__":
    GPIO.setup_leds()
    GPIO.turn_off_all_led()

    GPIO.blink_alert_led(on_time=0.05, off_time=0.05)

    sleep(10)

    SETUP = setup()

    if isinstance(SETUP, str):
        print(SETUP)
        print("Error occured")
        GPIO.error()
        
        sleep(10)

        os.system('sudo python3 /home/pi/printer/main.py')
    else:
        with open("/home/pi/printer/conf/conf.json", "r") as conf:
            configuration = json.load(conf)

            URL = configuration.get("ticketbutler").get("URL")

            ws = WS(SETUP)

            ws.ws_connect(URL, SETUP["printer_uuid"])
