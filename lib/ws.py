import websocket
import json

from lib.brother_ql_send import print_label
from lib.GPIO import GPIO

class WS:
    def __init__(self, config):
        self.__config = config
        self.__text_fields = config.get("textfields")

    def on_message(self, ws, message):
        response = json.loads(message)
        text_to_print = []
        skip = False

        for text in self.__text_fields:
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
                label=self.__config["label"],
                template=self.__config["template"],
                printer=self.__config["printer"],
                cut=self.__config["cut"],
                red=self.__config["red"],
                dpi_600=self.__config["dpi_600"],
                rotate="90"
            )
        else:
            print("Skipping print")
    
    def on_error(self, ws, error):
        GPIO.error()
        print("Error: ", error)

    def on_open(self, ws):
        GPIO.OK()
        print("Websocket Opened")

    def on_close(self, ws):
        GPIO.connecting()
        print("Websocked closed")

    def ws_connect(self, URL, printer_id):
        print("Connecting")

        ws = websocket.WebSocketApp(URL + "/" + printer_id + "/", 
            on_message=self.on_message,
            on_error=self.on_error,
            on_open=self.on_open,
            on_close=self.on_close)

        print("Connected")

        while True:
            ws.run_forever()