from io import BytesIO

from django.core.files import File
from PIL import Image


def resize_image(full_image, size):
    image_name = full_image.name
    image = Image.open(full_image)
    image = image.resize(size, Image.ANTIALIAS)

    image_io = BytesIO()
    image.save(image_io, format="png")
    new_image = File(image_io, name=image_name)
    return new_image


def convert_image_webp(full_image):
    image_name = full_image.name
    image_name = image_name.replace(".jpg", ".webp")
    image_name = image_name.replace(".png", ".webp")
    image = Image.open(full_image)

    image_io = BytesIO()
    image.save(image_io, format="webp", optimize=True, quality=50)
    new_image = File(image_io, name=image_name)
    return new_image


def convert_image_webp_with_resize(full_image, size):
    image_name = full_image.name
    image_name = image_name.replace(".jpg", ".webp")
    image_name = image_name.replace(".png", ".webp")
    image = Image.open(full_image)
    image = image.resize(size, Image.ANTIALIAS)

    image_io = BytesIO()
    image.save(image_io, format="webp", optimize=True, quality=50)
    new_image = File(image_io, name=image_name)
    return new_image


def resize_review_image(full_image, size):
    image_name = full_image.name
    image = Image.open(full_image)

    left = int(image.size[0] / 2 - 1720 / 2)
    upper = int(image.size[1] / 2 - 1140 / 2)
    right = left + 1720
    lower = upper + 1140

    # Crop the center of the image
    im_cropped = image.crop((left, upper, right, lower))
    image = im_cropped.resize(size, Image.ANTIALIAS)
    image_io = BytesIO()
    image.save(image_io, format="png")
    new_image = File(image_io, name=image_name)
    return new_image
