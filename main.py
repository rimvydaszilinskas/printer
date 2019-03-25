from brother_ql_send import print_label
import websocket
import json

# ws://ticketfix.moome.net/ws/print/<EVENT_ID>/<PRINTER_ID>/
PRINTER_IDENTIFIER = "1de5cba17b2b4ea0a21a40bddd6df9c1"
PROJECT_IDENTIFIER = "ceb26cac1fa2499cb782fbe26c6c72cf"
SOCKET_URL = "ws://ticketfix.moome.net/ws/print"

# dummy preset data
text = (
    {
        "text":"Name LastName",
        "fill":(0, 0, 0),
        "location":(38, 250),
        "font_size":84
    },
    {
        "text":"Position",
        "fill":(0, 0, 0),
        "location":(38, 400),
        "font_size":36
    }
)

# qr = {
#     "data": "http://google.com",
#     "box_size": 8,
#     "border": 1,
#     "inverted": False,
#     "location": (900, 450)
# }

ws = websocket.create_connection(SOCKET_URL + "/" + PROJECT_IDENTIFIER + "/" + PRINTER_IDENTIFIER + "/")

# should send some identifier data here

while True:
    response = ws.recv()
    resp = json.loads(response)

    print(resp)

    if "full_name" not in resp["message"] or "company_name" not in resp["message"]:
        print("No name and/or position supplied")
        continue

    text[0]["text"] = resp["message"]["full_name"]
    text[1]["text"] = resp["message"].get("company_name", "")
    # rotate 90 degrees to print it full size
    print_label(text=text, rotate="90")

ws.close()