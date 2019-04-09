from brother_ql_send import print_label
import websocket
import json
from image_generate import create_card

# Requires pklaus/brother_ql library to be installed
# https://github.com/pklaus/brother_ql

PRINTER_IDENTIFIER = "1de5cba17b2b4ea0a21a40bddd6df9c1"
PROJECT_IDENTIFIER = "b62dd5d67fca4a32ba2dbcf9963bcc48"
SOCKET_URL = "ws://ticketfix.moome.net/ws/print"

# dummy preset data
# text = (
#     {
#         "text":"full_name",
#         "fill":(0, 0, 0),
#         "location":(90, 385),
#         "font_size":84
#     },
#     {
#         "text":"company_name",
#         "fill":(0, 0, 0),
#         "location":(90, 470),
#         "font_size":36
#     }
# )

# qr = {
#     "data": "http://google.com",
#     "box_size": 8,
#     "border": 1,
#     "inverted": False,
#     "location": (900, 450)
# }


def on_message(ws, message):
    response = json.loads(message)
    print(response)

    if "full_name" not in response["message"] or "company_name" not in response["message"]:
        print("No name and/or position supplied")
    else:
        # text[0]["text"] = response["message"]["full_name"]
        # text[1]["text"] = response["message"].get("company_name", "")
        text = response["message"]["full_name"]
        
        # rotate 90 degrees to print it full size
        print_label(text=text, rotate="90", label="54", red=False)
        
#        create_card(target_file="./templates/test.png", text=text, save=True)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("Closed")

def on_open(ws):
    print("Opened")

ws = websocket.WebSocketApp(SOCKET_URL + "/" + PROJECT_IDENTIFIER + "/" + PRINTER_IDENTIFIER + "/",
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close,
                            on_open=on_open)

while True:
    ws.run_forever()