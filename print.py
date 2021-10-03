from PIL import Image, ImageDraw, ImageFont
from datetime import date, timedelta
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql import BrotherQLRaster
from brother_ql.devicedependent import label_type_specs


LABEL_SIZE = '29x90'
MODEL = "QL-570"
BACKEND = "linux_kernel"
PRINTER = "/dev/usb/lp0"
# BACKEND = "pyusb"
# PRINTER = "usb://0x04f9:0x2028"

def draw(dots, name, description, date):
    # Draw horizontally and rotate later
    image = Image.new("RGB", (dots[1], dots[0]), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", size=40)
    font_large = ImageFont.truetype("arial.ttf", size=100)

    draw.text((dots[1]/2, 10), description, font=font_large, fill="black", anchor="ma")
    date_text = "Expires: " + date.strftime("%d %b %Y")
    draw.text((10, 150), date_text, font=font, fill="black")
    draw.text((10, 200), "Owner: " + name, font=font, fill="black")

    return image


def send_to_printer(image):
    qlr = BrotherQLRaster(MODEL)
    qlr.exception_on_warning = True
    instructions = convert(
        qlr=qlr, 
        images=[image],    #  Takes a list of file names or PIL objects.
        label='29x90', 
        rotate='90',    # 'Auto', '0', '90', '270'
        threshold=70.0,    # Black and white threshold in percent.
        dither=False, 
        compress=False, 
        red=False,    # Only True if using Red/Black 62 mm label tape.
        dpi_600=False, 
        hq=True,    # False for low quality.
        cut=True
    )

    send(instructions=instructions, printer_identifier=PRINTER, backend_identifier=BACKEND, blocking=True)


def print_label(name, label_type):
    if label_type == "short_stay":
        expiry = date.today() + timedelta(days=10)
        description = "Short stay"
    elif label_type == "long_stay":
        expiry = date.today() + timedelta(days=30*2) # Roughly 2 months
        description = "Long stay"
    
    dots_printable = label_type_specs[LABEL_SIZE]["dots_printable"]
    image = draw(dots_printable, name, description, expiry)
    send_to_printer(image)

if __name__ == "__main__":
    now = date.today()
    name = "Test name"
    expiry = now + timedelta(days=30*2) # Roughly 2 months

    dots_printable = label_type_specs[LABEL_SIZE]["dots_printable"]
    image = draw(dots_printable, name, expiry)
    image.save("test.png")

    # send_to_printer(image)