'''
Retrieves the latest frontpage of the NYT and converts it to bmp format

Prerequisites:
- PyMuPDF (imported as fitz)
- Pillow (imported as PIL)
'''

import datetime as dt
import math
from random import randrange
import requests
import fitz
from PIL import Image

out = "tmp.jpg"

show_random_page = True

if show_random_page:
    attempts = 5
    while attempts > 0:
        attempts -= 1
        random_day = randrange(365 * 8)  # random day in the past 8 years
        url = f"https://static01.nyt.com/images/{(dt.datetime.today() - dt.timedelta(days=random_day)).strftime('%Y/%m/%d')}/nytfrontpage/scan.pdf"
        response = requests.get(url)
        if response.status_code == 200:
            attempts = 0

else:
    # Get todays frontpage
    url = f"https://static01.nyt.com/images/{dt.datetime.today().strftime('%Y/%m/%d')}/nytfrontpage/scan.pdf"
    response = requests.get(url)

    if response.status_code != 200:
        # Try to get yesterdays frontpage instead:
        url = f"https://static01.nyt.com/images/{(dt.datetime.today() - dt.timedelta(days=1)).strftime('%Y/%m/%d')}/nytfrontpage/scan.pdf"
        response = requests.get(url)

if response.status_code != 200:
    raise Exception("Unable to retrieve nyt frontpage")

pdf_tmp = "nyt_frontpage.pdf"
with open(pdf_tmp, 'wb') as f:
    f.write(response.content)

# Convert pdf to png
pdffile = pdf_tmp
doc = fitz.open(pdffile)
page = doc.loadPage(0)  # number of page
zoom = 2 # zoom factor to increase output quality
mat = fitz.Matrix(zoom, zoom)
pix = page.getPixmap(matrix = mat)

# Apply transformations and save to bmp
# Target dimensions: 1872×1404
img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
img = img.rotate(90, expand = True)

# Resize
max_width = 1872
max_height = 1404
input_width = img.width
input_height = img.height
resize_factor = max_height / input_height
resize_width = math.floor(input_width * resize_factor)
img = img.resize((1872, 1404), Image.HAMMING, (0, 0, resize_width, input_height))

img = img.rotate(180, expand = True)

# file_out = "tmpbmp.bmp"
file_out = "../../controller/it8951/main/tmpbmp.bmp"
img.save(file_out)

t=2