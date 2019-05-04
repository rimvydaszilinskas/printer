import requests
import json
import urllib.request
import os
import websocket
from gpiozero import LED

from brother_ql_send import print_label
import guess_device

# Global variables for use in callbacks
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
    "template": "./templates/default.png",
    "printer": "QL-810W",
    "cut": True,
    "qr": None
}

USE_GPIO = False

# Load image to be passed down
TEMPLATE = None

def dump_data(printer_to_dump):
    # update device.json file with printer_to_dump
    printer = {
        "id": printer_to_dump.get("id"),
        "identifier": printer_to_dump.get("identifier"),
        "createdAt": printer_to_dump.get("createdAt"),
        "image_url": printer_to_dump.get("image_url", None)
    }

    with open("./conf/device.json", "w") as outfile:
        json.dump(printer, outfile)

    print("New device data saved.")

def load_image(): 
    TEMPLATE = open('./templates/' + PRINT_CONFIG.get('template', './templates/default.png'))

def cleanup_templates(directory="./templates"):
    # deletes all the files that re not default.png
    for root, dirs, files in os.walk(directory):  
        for filename in files:
            if filename != "default.png" and filename != "template.bmp":
                os.remove(directory + '/' + filename)

def template_exist(event_id):
    return os.path.isfile("./templates/" + event_id + ".png")

def download_template(url, event_id):
    urllib.request.urlretrieve(url, "./templates/" + event_id + ".png")
    return "./templates/" + event_id + ".png"

def on_message(ws, message):
    response = json.loads(message)
    text_to_print = []
    skip = False

    for text in TEXT_FIELDS:
        if text.get("placeholder") not in response["message"]:
            skip = True
            break
        else:
            text['text'] = response["message"][text.get("placeholder")]
            text_to_print.append(text)

    if not skip:
        print_label(
            text=text_to_print, 
            qr=None, 
            label=PRINT_CONFIG["label"], 
            template=PRINT_CONFIG["template"], 
            printer=PRINT_CONFIG["printer"],
            cut=PRINT_CONFIG["cut"],
            red=PRINT_CONFIG["red"],
            dpi_600=PRINT_CONFIG['dpi_600'],
            rotate="90")

def on_error(ws, error):
    print("Error: " + error)

def on_close(ws):
    print("Websocket closed")

def on_open(ws):
    print("Websocket Opened")

def connect(URL, event_id, printer_id):
    printer_id = printer_id.replace("-", "")

    if event_id is not None:
        event_id = event_id.replace("-", "")
    else:
        print("No event id supplied. Exiting now")
        exit()
    # main entry point to socket application
    print("Connection: " + URL + "/" + event_id + "/" + printer_id)

    ws = websocket.WebSocketApp(URL + "/" + event_id + "/" + printer_id,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open)
    
    # force to keep connection alive
    while True:
        ws.run_forever()

if __name__ == "__main__":
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

    USE_GPIO = guess_device.guess_device() == "rpi"
    
    config_file = open("./conf/conf.json")
    device_file = open("./conf/device.json")

    config = json.load(config_file)
    device = json.load(device_file)

    config_file.close()
    device_file.close()

    request = requests.post(config.get("registration").get("URL"), data={ "secret": config.get("registration").get("secret"), "identifier": device.get("identifier") })

    if request.status_code == 200:
        print("Status 200: OK")
        response = json.loads(request.text)

        printer = response.get("response")

        if device.get("id", None) != printer.get("id"):
            # rewrite device json
            dump_data(printer)

        events = printer.get("events")

        if len(events) != 0:
            event = events[0]
            event_id = event.get("id")
            ticketbutler_id = event.get("tbid")
            template = event.get("template")

            if template is not None:
                image_url = template.get("image", None)
                PRINT_CONFIG["label"] = template.get("label", PRINT_CONFIG["label"])
                PRINT_CONFIG["red"] = template.get("red", PRINT_CONFIG["red"])
                PRINT_CONFIG["dpi_600"] = template.get("dpi_600", PRINT_CONFIG["dpi_600"])
                # PRINT_CONFIG["font"] = template.get("font", None)
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

                # if template is not present download it
                if image_url != None or image_url != "":
                    cleanup_templates()
                    PRINT_CONFIG["template"] = "./templates/" + event_id + ".png"

                    if not template_exist(event_id=event_id) or device['image_url'] != image_url:
                        print("Template does not exist.")

                        PRINT_CONFIG["template"] = download_template(url=image_url, event_id=event_id)
                        print("Template downloaded")

                        printer['image_url'] = image_url
                        dump_data(printer)
                        print("Printer data updated")
                    else:
                        print("Template exsists. No new data saved.")

            connect(config['ticketbutler']['URL'], ticketbutler_id, printer.get('id'))
        else:
            # no active events
            cleanup_templates()
    elif request.status_code == 201:
        # Created status
        # update the device.json and continue add delay for another request
        print("Status 201: Created")

        response = json.loads(request.text)

        printer = response.get("response")

        dump_data(printer)

        cleanup_templates()
        print("Printer data dumped. Waiting for restart")
    else:
        # Error status
        # Restart the application
        response = json.loads(request.text)
        print("Error " + {response.get('status')} + ": " + {response.get('message', response.get('response'))})
        print("Waiting for restart")