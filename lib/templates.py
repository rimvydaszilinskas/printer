import os
import urllib.request

def load_image(template):
    print(template)
    return open(os.getcwd() + "\\templates\\" + template)

def cleanup_templates():
    for root, dirs, files in os.walk(os.getcwd() + "\\templates"):
        for filename in files:
            if filename != "default.png" and filename != "template.bmp":
                os.remove(os.getcwd() + "\\templates\\" + filename)

def download_template(url, event_id):
    urllib.request.urlretrieve(url, os.getcwd() + "\\templates\\" + event_id + ".png")
    return "./templates/" + event_id + ".png"

def template_exist(event_id):
    return os.path.isfile(os.getcwd() + "\\templates\\" + event_id + ".png")