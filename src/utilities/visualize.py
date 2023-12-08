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


# Draw annotations on image
def draw_annotations(image_path, annotations, output_folder):
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


def visualize_dataset(data, output_folder):
    image_path = data["data"]["image"]
    annotations = data["annotations"]

    draw_annotations(image_path, annotations, output_folder)
