from brother_ql_send import print_label
from image_generate import create_card

text = (
    {
        "text":"Rimvydas Zilinskas",
        "fill":(0, 0, 0),
        "location":(90, 385),
        "font_size":64
    },
    {
        "text":"Developer",
        "fill":(0, 0, 0),
        "location":(90, 457),
        "font_size":24
    }
)

print_label(text=text, rotate="90", label="54")

# create_card(target_file="./templates/test.png", text=text, save=True)