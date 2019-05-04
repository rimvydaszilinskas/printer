from brother_ql_send import print_label
from image_generate import generate_card

text = (
    {
        "text":"",
        "fill":(0, 0, 0),
        "location":(0, 0),
        "font_size":64
    },
    {
        "text":"",
        "fill":(0, 0, 0),
        "location":(0, 0),
        "font_size":24
    }
)

print_label(text=text, rotate="90", label="54", red=False, template="./templates/tedx.png", dpi_600=True, cut=False)

print_label(text=text, rotate="90", label="54", red=False, template="./templates/tedx.png", dpi_600=True)
# create_card(target_file="./templates/tedx.png", text=text, save=True)