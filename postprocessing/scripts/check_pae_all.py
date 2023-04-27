#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
from PIL import Image, ImageDraw, ImageFont
import os

def concatenate_images(folder_path, title_font_size=16):
    # Get all PNG files in the directory
    image_files = glob.glob(f'{folder_path}/*.png')

    # Open all images
    images = [Image.open(img) for img in image_files]

    # Get dimensions of the first image
    width, height = images[0].size

    # Create a new image with the same width and the combined height of all images
    result = Image.new('RGB', (width, height * len(images)), color='white')

    # Paste each image into the result image vertically
    for i, img in enumerate(images):
        result.paste(img, (0, i * height))

    # Add a title to each image
    title_font = ImageFont.load_default()
    draw = ImageDraw.Draw(result)
    title_font_size = 24
    for i, img_file in enumerate(image_files):
        label = os.path.basename(img_file)
        label_width, label_height = draw.textsize(label, font=title_font)
        draw.text((0, i * height), label, font=title_font, fill=(0, 0, 0))

    return result

folder_path = './'
result = concatenate_images(folder_path)
result.save('result.png')

