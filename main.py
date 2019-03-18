from brother_ql_send import print_label
import socketio

URL = "http://localhost"
PORT = "3000"

socket = socketio.Client()

@socket.on("connect")
def init():
    print()

@socket.on("data")
def receive(data):
    pass

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

# print_label(text=text, qr=qr)

socket.connect(URL + ":" + PORT)