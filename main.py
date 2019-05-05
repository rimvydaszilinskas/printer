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

    SETUP = setup()

    if isinstance(SETUP, str):
        print("Error occured")
        GPIO.error()
        sleep(5)
    else:
        with open(ROOT_DIR + "/conf/conf.json", "r") as conf:
            configuration = json.load(conf)

            URL = configuration.get("ticketbutler").get("URL")

            ws = WS(SETUP)

            ws.ws_connect(URL, SETUP["printer_uuid"])
