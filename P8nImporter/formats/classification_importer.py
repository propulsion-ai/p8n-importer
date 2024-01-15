import json
import os
import shutil
import io
import base64
from PIL import Image

from ..config.logging import logger
from ..formats.base_importer import BaseImporter
from ..utilities.mapping import generate_labels_mapping
from ..utilities.visualize import draw_class_name


class ImageClassificationImporter(BaseImporter):
    def __init__(self, root_folder, output_folder):
        """
        Initialize ImageClassificationImporter object.

        Args:
            root_folder (str): Path to the root folder containing class folders.
            output_folder (str): Path to the output folder where the label_studio.json file will be saved.
        """
        super().__init__(root_folder, output_folder)
        self.files_folder = os.path.join(self.output_folder, "files")
        if not os.path.exists(self.files_folder):
            os.makedirs(self.files_folder)

    def visualize(self, data):
        """
        Visualizes the dataset.

        Args:
            data (dict): The dataset.
            output_folder (str): The path to the output folder.
        """
        image_path = data["data"]["image"]
        class_name = data["annotations"][0]["value"]["choices"][0]

        draw_class_name(image_path, class_name, self.output_folder)

    def import_task(self, image, class_name):
        """
        Import a single image classification task.

        Args:
            image (str or bytes or numpy.ndarray): The image to import as a task.
            class_name (str): The class name.
        """
        if not image:
            raise ValueError("Image is required")
        
        if not class_name:
            raise ValueError("Class name is required")

        if isinstance(image, bytes):
            image = Image.open(io.BytesIO(image))
        elif isinstance(image, str):
            if image.startswith("data:image"):
                _, encoded = image.split(",", 1)
                image = Image.open(io.BytesIO(base64.b64decode(encoded)))
            else:
                image = Image.open(image)

        image_name = os.path.basename(image.filename)
        image_path = os.path.join(self.files_folder, image_name)
        image.save(image_path)

        label_studio_item = {
            "data": {
                "image": os.path.relpath(image_path, self.output_folder),
                "annotations": [
                    {
                        "value": {"choices": [class_name]},
                        "from_name": "choice",
                        "to_name": "image",
                        "type": "choices",
                        "origin": "manual",
                    }
                ],
            },
        }

        output_file = os.path.join(self.output_folder, "dataset.json")
        with open(output_file, "w") as f:
            json.dump([label_studio_item], f, indent=4)

        self.generate_metadata([label_studio_item])

    def import_dataset(self):
        """
        Import the image classification dataset and generate the label_studio.json file.
        """
        label_studio_json = []

        for class_name in os.listdir(self.source_folder):
            class_folder = os.path.join(self.source_folder, class_name)
            if os.path.isdir(class_folder):
                for image_file in os.listdir(class_folder):
                    image_path = os.path.join(class_folder, image_file)
                    target_image_path = os.path.join(self.files_folder, image_file)

                    try:
                        # Copy image file to files folder
                        shutil.copy2(image_path, target_image_path)
                    except FileNotFoundError:
                        logger.warning(
                            f"Image file not found in: {image_path}. Skipping..."
                        )
                        continue

                    label_studio_item = {
                        "data": {
                            "image": os.path.relpath(
                                target_image_path, self.output_folder
                            ),
                            "annotations": [
                                {
                                    "value": {"choices": [class_name]},
                                    "from_name": "choice",
                                    "to_name": "image",
                                    "type": "choices",
                                    "origin": "manual",
                                }
                            ],
                        },
                    }

                    label_studio_json.append(label_studio_item)

        output_file = os.path.join(self.output_folder, "dataset.json")
        with open(output_file, "w") as f:
            json.dump(label_studio_json, f, indent=4)

        self.generate_metadata(label_studio_json)

    def generate_metadata(self, data):
        """
        Generate the metadata of the dataset.

        Args:
            data (list): The dataset.
        """
        labels = set()
        for item in data:
            annotation = item["data"]["annotations"][0]
            label = annotation["value"]["choices"][0]
            labels.add(label)

        labels_mapping = generate_labels_mapping(labels, has_colors=False)
        labels_mapping_file = os.path.join(self.output_folder, "metadata.json")
        with open(labels_mapping_file, "w") as f:
            json.dump(labels_mapping, f, indent=4)

    def get_input_action_types(self):
        """
        Get the input and action types of the dataset.

        Returns:
            tuple: The input and action types.
        """
        return "IMAGE", "IMAGE_CLASSIFICATION"
