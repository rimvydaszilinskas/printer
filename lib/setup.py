import json
import os
from time import sleep
import sys

import requests

from lib.GPIO import GPIO
from lib.templates import cleanup_templates, download_template, template_exist

def dump_data(printer_to_dump):
    GPIO.writing()

    printer = {
        "id": printer_to_dump.get("id"),
        "identifier": printer_to_dump.get("identifier"),
        "image_url": printer_to_dump.get("image_url", None)
    }

    with open("/home/pi/printer/conf/device.json", "w") as outfile:
        json.dump(printer, outfile)
    
    print("New device data saved.")

    GPIO.OK()

def handle_201(response):
    GPIO.created()

    print("Status 201: Created")

    dump_data(response)
    cleanup_templates()

    return None

def handle_200(response, device, config):
    GPIO.turn_ok_led(on=True)

    TEXT_FIELDS = [
        {
            "text": "full_name",
            "placeholder": "full_name",
            "location": (0, 0),
            "align": "right",
            "font_size": 84
        }
    ]

    PRINT_CONFIG = {
        "rotate": "90",
        "label": "62",
        "red": False,
        "dpi_600": False,
        "template": "/home/pi/printer/templates/default.png",
        "font": "/home/pi/printer/fonts/Sanseriffic.otf",
        "printer": "QL-810W",
        "cut": True,
        "qr": None
    }

    print("Status 200: OK")

    printer = response.get("response")

    PRINT_CONFIG["printer_uuid"] = response.get("response").get("id")

    if device.get("id", None) != printer.get("id"):
        # rewrite device json
        dump_data(printer)

    events = printer.get("events")

    if len(events) != 0:
        GPIO.blink_alert_led(on_time=0.1, off_time=0.1)

        event = events[0]
        event_id = event.get("id")
        ticketbuttler_id = event.get("tbid")
        template = event.get("template")

        if template is not None:
            image_url = template.get("image", None)

            PRINT_CONFIG["label"] = template.get("label", PRINT_CONFIG["label"])
            PRINT_CONFIG["red"] = template.get("red", PRINT_CONFIG["red"])
            PRINT_CONFIG["dpi_600"] = template.get("dpi_600", PRINT_CONFIG["dpi_600"])

            textfields = template.get("textfields")

            if len(textfields) != 0:
                TEXT_FIELDS = []

                for textfield in textfields:
                    TEXT_FIELDS.append({
                        "text": textfield.get("placeholder"),
                        "placeholder": textfield.get("placeholder"),
                        "location": (textfield.get("x"), textfield.get("y")),
                        "font_size": textfield.get("font_size"),
                        "align": textfield.get("align")
                    })

            if image_url != None or image_url != "":
                cleanup_templates()
                PRINT_CONFIG["templates"] = "/home/pi/printer/templates/" + event_id + ".png"
                
                if not template_exist(event_id=event_id) or device["image_url"] != image_url:
                    print("Template does not exist.")

                    if image_url:
                        PRINT_CONFIG["template"] = download_template(url=image_url, event_id=event_id)
                    
                    print("Template downloaded")

                    printer["image_url"] = image_url
                    dump_data(printer)
                    print("Printer data updated")
                else:
                    print("Template exists. No new data saved.")
            else:
                print("No image url")
        else:
            print("No defined template")
    else:
        # no active events
        print("No active event")
    
    PRINT_CONFIG["textfields"] = TEXT_FIELDS

    GPIO.OK()
    return PRINT_CONFIG

def handle_error(response):
    GPIO.error()

    print("Error " + {response.get('status')} + ": " + {response.get('message', response.get('response'))})
    print("Waiting for restart")

    return None

def setup():
    """
    Init sequence:
        1. Check the event last initialized
        2. Load the data from the API
        3. Compare if the data is already correct
            3.1. If it is correct - continue
            3.2. If it is not correct:
                3.2.1. Delete old image.
                3.2.1. Download the new image.
                3.2.2. Replace the old log with the new event log.
        4. Connect to socket
    """

    ROOT_PATH = os.getcwd()

    config_file = open("/home/pi/printer/conf/conf.json")
    device_file = open("/home/pi/printer/conf/device.json")
    
    config = json.load(config_file)
    device = json.load(device_file)

    try:
        request = requests.post(config.get("registration").get("URL"), data={
            "secret": config.get("registration").get("secret"),
            "identifier": device.get("identifier")
        })
        
        if request.status_code == 200:
            response = json.loads(request.text)

            return handle_200(response, device, config)
        elif request.status_code == 201:
            response = json.loads(request.text)

            return handle_201(response)
        else:
            response = json.loads(request.text)

            return handle_error(response)
    except:
        print(sys.exc_info())
        return "Error"
