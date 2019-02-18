import os

# Requires pklaus/brother_ql library to be installed
# https://github.com/pklaus/brother_ql

def print_label(image=None, model="QL-810W", printer="/dev/usb/lp0", length=62 ,monochrome=False):
    # function cannot continue without image
    if image is None:
        raise Exception("No image specified")
    
    # building the command
    cmd = f"brother_ql --model {model} --printer {printer} print -l {length} {image}"

    if not monochrome:
        cmd += f" --red"

    output = os.popen(cmd)

    return output

def is_monochrome(model):
    # only models starting with QL supports printing in red and requires --red flag
    if model.startswith("QL-"):
        return False
    return True
