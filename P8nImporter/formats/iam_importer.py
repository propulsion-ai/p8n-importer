# importing the iam dataset in fwf format

import json
import os
import shutil

import pandas as pd

from ..config.logging import logger
from ..formats.base_importer import BaseImporter
from ..utilities.mapping import generate_labels_mapping
from ..utilities import generate_random_id


class IAMImporter(BaseImporter):
    def __init__(self, root_folder, output_folder):
        """
        Initialize the IAMImporter class.

        Args:
            root_folder (str): The root folder path.
            output_folder (str): The output folder path.
        """
        super().__init__(root_folder, output_folder)
        self.files_folder = os.path.join(self.output_folder, "files")
        if not os.path.exists(self.files_folder):
            os.makedirs(self.files_folder)

    def import_dataset(self):
        """
        Imports a fixed-width file dataset and generates a json.

        Raises:
            Exception: If the schemas of the files are not consistent.
        """
        label_studio_json = []

        # Raise exception if self.source_folder is a directory
        if os.path.isdir(self.source_folder):
            raise Exception("The source must be a txt file.")

        # Read the txt file using pandas fwf
        try:
            df = pd.read_fwf(self.source_folder, header=None)
            df.rename(columns={0: "file_name", 1: "text"}, inplace=True)
            del df[2]
            # some file names end with jp instead of jpg, let's fix this
            df["file_name"] = df["file_name"].apply(
                lambda x: x + "g" if x.endswith("jp") else x
            )
        except Exception as e:
            logger.error(f"Error reading the file {self.source_folder}. {e}")
            raise e

        # Create the json in the Label Studio format with 3 annotations per image
        for index, row in df.iterrows():
            # find the width and height of the image
            image_path = row[0]

            # get parent directory of the self.source_folder
            parent_directory = os.path.dirname(self.source_folder)
            image_path = os.path.join(parent_directory, "image", image_path)
            image_file = os.path.basename(image_path)
            target_image_path = os.path.join(self.files_folder, image_file)

            try:
                # Copy image file to files folder
                shutil.copy2(image_path, target_image_path)
            except FileNotFoundError:
                logger.error(f"Image file not found: {image_path}")
                raise

            # get the width and height of the image
            from PIL import Image

            img = Image.open(image_path)
            width, height = img.size
            # width, height = self.get_image_width_height(image_path)

            # generate a random id like UkpXpzQrEO
            id = generate_random_id()

            # create the bbox annotation
            bbox_annotation = {
                "original_width": width,
                "original_height": height,
                "image_rotation": 0,
                "value": {
                    "x": 0,
                    "y": 0,
                    "width": width,
                    "height": height,
                    "rotation": 0,
                },
                "id": id,
                "from_name": "bbox",
                "to_name": "image",
                "type": "rectangle",
                "origin": "manual",
            }

            # create the label annotation
            label_annotation = {
                "original_width": width,
                "original_height": height,
                "image_rotation": 0,
                "value": {
                    "x": 0,
                    "y": 0,
                    "width": width,
                    "height": height,
                    "rotation": 0,
                    "labels": ["Text"],
                },
                "id": id,
                "from_name": "label",
                "to_name": "image",
                "type": "labels",
                "origin": "manual",
            }

            # create the transcription annotation
            transcription_annotation = {
                "original_width": width,
                "original_height": height,
                "image_rotation": 0,
                "value": {
                    "x": 0,
                    "y": 0,
                    "width": width,
                    "height": height,
                    "rotation": 0,
                    "text": [row[1]],
                },
                "id": id,
                "from_name": "transcription",
                "to_name": "image",
                "type": "textarea",
                "origin": "manual",
            }

            # create the label studio item
            label_studio_item = {
                "data": {
                    "image": os.path.relpath(target_image_path, self.output_folder),
                    "annotations": [
                        bbox_annotation,
                        label_annotation,
                        transcription_annotation,
                    ],
                }
            }

            label_studio_json.append(label_studio_item)
        # Save the json
        output_file = os.path.join(self.output_folder, "dataset.json")
        with open(output_file, "w") as f:
            json.dump(label_studio_json, f, indent=4)

        self.generate_metadata(label_studio_json)

    def generate_metadata(self, data):
        """
        Generate the metadata of the dataset.

        Args:
            data (list): The dataset as an array of objects.
        """
        labels = set()
        for item in data:
            for annotation in item["data"]["annotations"]:
                if annotation["from_name"] == "label":
                    for label in annotation["value"]["labels"]:
                        labels.add(label)

        labels_mapping = generate_labels_mapping(labels)
        labels_mapping_file = os.path.join(self.output_folder, "metadata.json")
        with open(labels_mapping_file, "w") as f:
            json.dump(labels_mapping, f, indent=4)

    def get_image_width_height(image_path):
        """
        Get the width and height of the image.

        Args:
            image_path (str): The path to the image.

        Returns:
            tuple: The width and height of the image.
        """
        from PIL import Image

        img = Image.open(image_path)
        return img.size

    def get_input_action_types(self):
        """
        Get the input and action types of the dataset.

        Returns:
            tuple: The input and action types.
        """
        return "IMAGE", "IMAGE_CHARACTER_RECOGNITION"
