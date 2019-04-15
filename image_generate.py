import qrcode
from PIL import Image, ImageFont, ImageDraw

def generate_qr(data, box_size=8, border=1, inverted = False, save = False, filename = False):
    # returns the qrcode.image.pil.PilImage object
    # can apply methods like .save(filename)
    qr = qrcode.QRCode(
        box_size=box_size,
        border=border
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color = "black" if not inverted else "white", back_color = "white" if not inverted else "black")

    if save:
        if filename is None:
            img.save("./output/QR.png")
        else:
            img.save("./output/" + filename)

    return img

def paste_image(target, img, location):
    # pastes image on top of another image
    target.paste(img, location)
    return target

def write_text(target_file, text, location, fill=(255, 255, 255), font="./fonts/Sanseriffic.otf", font_size=16, save=False, dest_filename=None):
    # Write on top of image
    if isinstance(target_file, str):
        img = Image.open(target_file)
    else:
        img = target_file
    
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(font, font_size)
    draw.text(location, text, font=font, fill=fill)
    
    if save:
        if dest_filename is None:
            filename = target_file.split(".")
            if(len(filename) == 3):
                dest_filename = "./output/" + filename[0] + "_edit." + filename[1]
        
        img.save("./output/" + dest_filename)

    return img

def write_text_middle(target_file, text, y, fill=(255, 255, 255), font="./fonts/Sanseriffic.otf", font_size=16, save=False, dest_filename=None):
    draw = ImageDraw.Draw(target_file)

    font = ImageFont.truetype(font, font_size)

    W, H = target_file.size

    w, h = draw.textsize(text, font=font)

    location = ((W - w) / 2, y)

    draw.text(xy=location, text=text, fill=fill, font=font)

def create_card(target_file, text, qr=None, font="./fonts/BalooChettan-Regular.ttf", save=False, dest_filename=None):
    # returns image item if save is False
    # returns filepath to the file saved if save is True
    img = Image.open(target_file)

    # if text is a touple then iterate and print all text on the template
    if type(text) is tuple:
        for output in text:
            img = write_text(
                target_file=img, 
                text=output["text"],
                fill=output["fill"],
                location=output["location"], 
                font_size=output["font_size"], 
                save=False, 
                font=font
            )
    else:
        img = write_text(
            target_file=img, 
            text=text["text"], 
            fill=text["fill"], 
            location=text["location"], 
            font_size=text["font_size"], 
            save=False
        )

    def __paste_qr(QR, img):
        # paste in the qr code in the down right corner
        img_width, img_height = img.size
        QR_width, QR_height = QR.size
        offset_width = img_width - QR_width - 50
        offset_height = img_height - QR_height - 50
        paste_image(img, QR, (offset_width, offset_height))

        return img

    if qr is not None:
        if isinstance(qr, str):
            QR = generate_qr(qr)
            __paste_qr(QR, img)
        elif isinstance(qr, dict):
            QR = generate_qr(data=qr["data"], box_size=qr["box_size"], border=qr["border"], inverted=qr["inverted"], save=False)
            if "location" in qr:
                paste_image(img, QR, qr["location"])
            else:
                __paste_qr(QR, img)

    if save:
        if dest_filename is not None and isinstance(dest_filename, str):
            img.save("./output/" + dest_filename)
            return "./ouput/" + dest_filename
        else:
            img.save("./output/default1.png")
            return "./output/default.png"
    else:
        return img

# def write_text(target_file, text, location, fill=(255, 255, 255), font="./fonts/Sanseriffic.otf", font_size=16, save=False, dest_filename=None):

def create_card_middle(target_file, text, top=100, fill=(255, 255, 255), font_size=80, font_location="./fonts/Lato-Bold.ttf"):
    # prints the name in the middle of image, pushed down by <top>px
    img = Image.open(target_file)

    draw = ImageDraw.Draw(img)

    W, H = img.size

    font = ImageFont.truetype(font=font_location, size=font_size)
    w, h = draw.textsize(text, font=font)
    
    location = ((W - w) / 2, top)

    draw.text(xy=location, text=text, fill=fill, font=font)

    return img

def generate_card(target_file, text):
    img = Image.open(target_file)

    for txt in text:
        if txt["align"] == "center":
            write_text_middle(img, txt["text"], y=txt["location"][1], font_size=txt["font_size"], fill=(0,0,0))
        elif txt["align"] == "right":
            write_text(img, txt["text"], location=txt["location"], fill=(0, 0, 0), font_size=txt["font_size"])
    return img
# create_card(target_file="test.bmp", qr=qr, text=text, save=True)