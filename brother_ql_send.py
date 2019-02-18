from brother_ql.backends.helpers import send
from brother_ql.backends import guess_backend
from brother_ql.conversion import convert
from brother_ql.raster import BrotherQLRaster
from image_generate import create_card

def print_label(text, qr, printer_identifier="/dev/usb/lp0", template="./templates/test.bmp", printer="QL-810W", cut=True, red=True, dpi_600=True, rotate="90"):
    # create a card from the template
    card = create_card(target_file=template, text=text, qr=qr, save=False)

    # convert the card to raster
    qlr = BrotherQLRaster(printer)
    qlr.exception_on_warning = True

    images = [card]

    instructions = convert(qlr=qlr, images=images, label="62", cut=cut, red=red, dpi_600=dpi_600, rotate=rotate)
    # get the backend identifier
    backend_identifier = guess_backend(printer_identifier)

    # send the commands to the printer
    send(instructions=instructions, printer_identifier=printer_identifier, backend_identifier=backend_identifier)