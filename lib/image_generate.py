import qrcode
from PIL import Image, ImageFont, ImageDraw

def generate_card(target_file, text, font=None, save=False, dest_filename=None):
    if isinstance(target_file, str):
        image_file = Image.open(target_file)
    else:
        image_file = target_file

    if isinstance(text, list):
        for txt in text:
            write_text(txt, image_file, font_input=font)
    elif isinstance(text, dict):
        write_text(text, image_file, font_input=font)

    return image_file

def paste_image(target, image, location):
    target.paste(image, location)
    return target

def generate_qr(data, box_size=8, border=1, inverted = False, save = False, filename = False):
    # returns the qrcode.image.pil.PilImage object
    qr = qrcode.QRCode(
        box_size=box_size,
        border=border
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color = "black" if not inverted else "white", back_color = "white" if not inverted else "black")

    if save:
        if filename is None:
            img.save("/home/pi/printer/output/QR.png")
        else:
            img.save("/home/pi/printer/output/" + filename)

    return img

def write_text(text, image, font_input=None, fill=(0, 0, 0)):
    draw = ImageDraw.Draw(image)

    W, H = image.size

    font = ImageFont.truetype(font_input if font_input is not None else '/home/pi/printer/fonts/Sanseriffic.otf', text['font_size'])

    if text['align'] == 'right':
        location = text['location']

        w, h = draw.textsize(text['text'], font=font)

        while location[0] + w > W * 0.95:
            text['font_size'] -= 2
            font = ImageFont.truetype(font_input if font_input is not None else '/home/pi/printer/fonts/Sanseriffic.otf', text['font_size'])

            w, h = draw.textsize(text['text'], font=font)
    else:
        wT, hT = draw.textsize(text['text'], font=font)
        
        w, h = draw.textsize(text['text'], font=font)

        while w > (0.8 * W):
            text['font_size'] -= 2

            font = ImageFont.truetype(font_input if font_input is not None else '/home/pi/printer/fonts/Sanseriffic.otf', text['font_size'])

            w, h = draw.textsize(text['text'], font=font)


        location = ((W - wT) / 2, text['location'][1])

    draw.text(xy=location, text=text['text'], fill=fill, font=font)