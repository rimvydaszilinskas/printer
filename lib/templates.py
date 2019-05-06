import os
import urllib.request

def load_image(template):
    print(template)
    return open("/home/pi/printer/templates/" + template)

def cleanup_templates():
    for root, dirs, files in os.walk("/home/pi/printer/templates"):
        for filename in files:
            if filename != "default.png" and filename != "template.bmp":
                os.remove("/home/pi/printer/templates/" + filename)

def download_template(url, event_id):
    urllib.request.urlretrieve(url, "/home/pi/printer/templates/" + event_id + ".png")
    return "/home/pi/printer/templates/" + event_id + ".png"

def template_exist(event_id):
    return os.path.isfile("/home/pi/printer/templates/" + event_id + ".png")