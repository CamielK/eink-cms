'''
Retrieves the latest frontpage of the NYT and converts it to bmp format

Prerequisites:
- pdf2image (pip install pdf2image)
- pdftoppm (sudo apt install poppler-utils)
'''

import datetime as dt
import sys
import math
from random import randrange
import requests
from pdf2image import convert_from_path
from PIL import Image

out = "tmp.jpg"

# show_random_page = True
show_random_page = False

# do_rotate_90 = True
do_rotate_90 = False


def debug(text):
    print(f"[{str(dt.datetime.now())}] {text}")
    sys.stdout.flush()


debug("Downloading URL")
if show_random_page:
    attempts = 5
    while attempts > 0:
        attempts -= 1
        random_day = randrange(365 * 8)  # random day in the past 8 years
        datestr = (dt.datetime.today() - dt.timedelta(days=random_day)).strftime('%Y/%m/%d')
        debug(f"Downloading random frontpage for {datestr}")
        url = f"https://static01.nyt.com/images/{datestr}/nytfrontpage/scan.pdf"
        response = requests.get(url)
        if response.status_code == 200:
            attempts = 0
        else:
            debug(f"Unable to find frontpage for {datestr}")

else:
    # Get todays frontpage
    url = f"https://static01.nyt.com/images/{dt.datetime.today().strftime('%Y/%m/%d')}/nytfrontpage/scan.pdf"
    response = requests.get(url)

    if response.status_code != 200:
        debug(f"Unable to get latest frontpage, trying yesterday instead")
        # Try to get yesterdays frontpage instead:
        url = f"https://static01.nyt.com/images/{(dt.datetime.today() - dt.timedelta(days=1)).strftime('%Y/%m/%d')}/nytfrontpage/scan.pdf"
        response = requests.get(url)

if response.status_code != 200:
    raise Exception("Unable to retrieve nyt frontpage")

debug("Saving to PDF")
pdf_tmp = "nyt_frontpage.pdf"
with open(pdf_tmp, 'wb') as f:
    f.write(response.content)

# Convert pdf to jpeg
debug("Converting to JPEG")
tmpjpg = 'nyt_frontpage.jpg'
pages = convert_from_path(
    pdf_tmp,
    dpi=200,
    use_cropbox=True,
    hide_annotations=True,
    # poppler_path=r"C:\Program Files\poppler\poppler-21.10.0\Library\bin"  # only if running in Windows
)
if len(pages) <= 0:
    raise Exception("Unable to parse pdf")
pages[0].save(tmpjpg, 'JPEG')

debug("Transforming image")
# Apply transformations and save to bmp
# Target dimensions: 1872×1404
# img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
img = Image.open(tmpjpg)

if do_rotate_90:
    img = img.rotate(90, expand = True)

# # Resize
max_width = 1872
max_height = 1404
input_width = img.width
input_height = img.height
if do_rotate_90:
    # Cut width
    resize_factor = max_height / input_height
    resize_width = math.floor(input_width * resize_factor)
    resize_height = input_height
else:
    # Cut height
    resize_factor = input_width / max_width
    resize_width = input_width
    resize_height = math.floor(max_height * resize_factor)

# do resize
img = img.resize((max_width, max_height), Image.HAMMING, (0, 0, resize_width, resize_height))

if do_rotate_90:
    img = img.rotate(180, expand = True)

debug("Saving to BMP")
# file_out = "tmpbmp.bmp"
file_out = "../../controller/it8951/main/tmpbmp.bmp"
img.save(file_out)

t=2