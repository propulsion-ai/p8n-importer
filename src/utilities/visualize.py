import os
import random

from PIL import Image, ImageDraw, ImageFont


def get_random_color():
    return "#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])


# Convert Label Studio annotations to rectangle coordinates
def get_rectangle_coords(annotation, img_width, img_height):
    x = annotation["value"]["x"] * img_width / 100
    y = annotation["value"]["y"] * img_height / 100
    width = annotation["value"]["width"] * img_width / 100
    height = annotation["value"]["height"] * img_height / 100

    x_min = x
    y_min = y
    x_max = x + width
    y_max = y + height

    return [x_min, y_min, x_max, y_max]


# Draw bounding boxes on image
def draw_bbox_image(image_path, annotations, output_folder):
    image_path = os.path.join(output_folder, image_path)
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    img_width, img_height = image.size
    label_colors = {}

    try:
        font = ImageFont.truetype("arial.ttf", 15)
    except IOError:
        font = ImageFont.load_default()

    for annotation in annotations:
        label = annotation["value"]["rectanglelabels"][0]
        if label not in label_colors:
            label_colors[label] = get_random_color()
        color = label_colors[label]

        rect_coords = get_rectangle_coords(annotation, img_width, img_height)
        draw.rectangle(rect_coords, outline=color, width=2)
        draw.text((rect_coords[0], rect_coords[1]), label, fill=color, font=font)

    image.show()

def draw_class_name(image_path, class_name, output_folder):
    """
    Draw the class name on the top left corner of the image.

    Args:
        image_path (str): Path to the image file.
        class_name (str): The class name to be drawn.
        output_folder (str): The path to the output folder.
    """
    image_path = os.path.join(output_folder, image_path)
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    text_color = get_random_color()

    # Drawing text on the top left corner
    draw.text((10, 10), class_name, fill=text_color, font=font)

    image.show()
