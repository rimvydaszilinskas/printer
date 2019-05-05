import os
import lib.templates as templates
from lib.ws import WS
from lib.setup import setup
import json

ROOT_DIR = os.getcwd()

if __name__ == "__main__":
    SETUP = setup()
    
    with open(ROOT_DIR + "\\conf\\conf.json", "r") as conf:
        configuration = json.load(conf)

        URL = configuration.get("ticketbutler").get("URL")

        ws = WS(SETUP)
        print(ws.get_config())
        ws.ws_connect(URL, SETUP["printer_uuid"])

        
