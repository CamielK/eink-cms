"""
Load a random picture from the archive and fits it to the screen
"""

import datetime as dt
import sys
from PIL import Image

out = "tmpbmp"

archive_path = "/home/photo_archive/"
# archive_path = "D:/Documents/fotoarchief/pi_archive/"

def debug(text):
    print(f"[{str(dt.datetime.now())}] {text}")
    sys.stdout.flush()

# Choose a random image from archive
import os, random
imgname = random.choice(os.listdir(archive_path))
# imgname = "20e39558-5632-4c3b-8990-00f99bac65ca.jpg"

# Load image
debug(f"Loading image: {imgname}")
imgpath = f"{archive_path}{imgname}"
img = Image.open(imgpath)
max_width = 1872
max_height = 1404


def flat(*nums):
    """Build a tuple of ints from float or integer arguments. """
    return tuple(int(round(n)) for n in nums)


class Size(object):
    def __init__(self, pair):
        self.width = float(pair[0])
        self.height = float(pair[1])

    @property
    def aspect_ratio(self):
        return self.width / self.height

    @property
    def size(self):
        return flat(self.width, self.height)


def thumbnail(img, size):
    """
    Builds a thumbnail by cropping out a maximal region from the center of the original with
    the same aspect ratio as the target size, and then resizing. The result is a thumbnail which is
    always EXACTLY the requested size
    """

    original = Size(img.size)
    target = Size(size)

    if target.aspect_ratio > original.aspect_ratio:
        # image is too tall: take some off the top and bottom
        scale_factor = target.width / original.width
        crop_size = Size((original.width, target.height / scale_factor))
        top_cut_line = (original.height - crop_size.height) / 2
        img = img.crop(flat(0, top_cut_line, crop_size.width, top_cut_line + crop_size.height))
    elif target.aspect_ratio < original.aspect_ratio:
        # image is too wide: take some off the sides
        scale_factor = target.height / original.height
        crop_size = Size((target.width / scale_factor, original.height))
        side_cut_line = (original.width - crop_size.width) / 2
        img = img.crop(flat(side_cut_line, 0, side_cut_line + crop_size.width, crop_size.height))

    return img.resize(target.size, Image.ANTIALIAS)


img = thumbnail(img, (max_width, max_height))


# Save output
debug("Saving to BMP")
# file_out = f"{out}.jpg"
# file_out = f"{out}.bmp"
file_out = f"../../controller/it8951/main/{out}.bmp"
img.save(file_out)

t=2