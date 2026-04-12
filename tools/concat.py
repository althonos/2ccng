import argparse
import glob
import os

import numpy
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("--output", required=True)
parser.add_argument("--offset", type=int, default=0)
parser.add_argument("--axis", type=int, choices=[0, 1], required=True)
parser.add_argument("layers", nargs="+")
args = parser.parse_args()

palette = None
images = []
for i, filename in enumerate(args.layers):
    image = Image.open(filename)
    if palette is None and image.getpalette() is not None:
        palette = image.copy()
    image = image.convert("RGBA")
    images.append(image)

if args.axis == 0:
    h = sum( image.size[0] for image in images ) + args.offset
    w = images[0].size[1]
    x = args.offset
    y = 0
else:
    h = images[0].size[0]
    w = sum( image.size[1] for image in images )
    x = args.offset
    y = 0

out = Image.new("RGBA", (h, w), "#ffffffff")
for image in images:
    out.paste(image, (x, y))
    if args.axis == 0:
        x += image.size[0]
    elif args.axis == 1:
        y += image.size[1]

if palette is not None:
    out = out.convert("RGB")
    out = out.quantize(palette=palette, dither=0)
folder = os.path.dirname(args.output)
os.makedirs(folder, exist_ok=True)
out.save(args.output)

