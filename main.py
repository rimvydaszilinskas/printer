from brother_ql_send import print_label
import websocket
import json

URL = "ws://localhost"
PORT = "3000"

# dummy preset data
text = (
    {
        "text":"Name LastName",
        "fill":(0, 0, 0),
        "location":(38, 250),
        "font_size":84
    },
    {
        "text":"Developer",
        "fill":(0, 0, 0),
        "location":(38, 400),
        "font_size":36
    }
)

qr = {
    "data": "http://google.com",
    "box_size": 8,
    "border": 1,
    "inverted": False,
    "location": (900, 450)
}

ws = websocket.create_connection(URL + ":" + PORT)

# should send some identifier data here

while True:
    response = ws.recv()
    resp = json.loads(response)

    if "full_name" not in resp or "company_name" not in resp:
        print("No name and/or position supplied")
        continue

    text[0]["text"] = resp["full_name"]
    text[1]["text"] = resp["company_name"]
    print_label(text=text, qr=qr)


ws.close()