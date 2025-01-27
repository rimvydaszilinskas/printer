from brother_ql.backends.helpers import send
from brother_ql.backends import guess_backend
from brother_ql.conversion import convert
from brother_ql.raster import BrotherQLRaster
from lib.image_generate import generate_card

def print_label(text, qr=None, label="54",printer_identifier="/dev/usb/lp0", template="/home/pi/printer/templates/test.png", printer="QL-810W", cut=True, red=True, dpi_600=True, rotate="0"):
    # create a card from the template
    # card = create_card(target_file=template, text=text, qr=qr, save=False)
    card = generate_card(target_file=template, text=text)
    
    # convert the card to raster
    qlr = BrotherQLRaster(printer)
    qlr.exception_on_warning = True

    # convert takes only an array
    images = [card]

    instructions = convert(qlr=qlr, images=images, label=label, cut=cut, red=red, rotate=rotate)
    # get the backend identifier
    backend_identifier = guess_backend(printer_identifier)

    # send the commands to the printer
    print("Sending instructions to print")
    send(instructions=instructions, printer_identifier=printer_identifier, backend_identifier=backend_identifier)