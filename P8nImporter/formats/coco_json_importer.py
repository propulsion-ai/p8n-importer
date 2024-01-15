import json
import os
import shutil

from ..formats.base_importer import BaseImporter
from ..config.logging import logger
from ..utilities.visualize import draw_bbox_image
from ..utilities.mapping import generate_labels_mapping


class COCOImporter(BaseImporter):
    def __init__(self, root_folder, output_folder):
        """
        Initialize COCOImporter object.

        Args:
            root_folder (str): Path to the root folder containing "train," "test," and "valid" folders.
            output_folder (str): Path to the output folder where the label_studio.json file will be saved.
        """
        super().__init__(root_folder, output_folder)
        self.files_folder = os.path.join(self.output_folder, "files")
        if not os.path.exists(self.files_folder):
            os.makedirs(self.files_folder)

    def visualize(self, data, output_folder):
        """
        Visualizes the dataset.

        Args:
            data (dict): The dataset.
            output_folder (str): The path to the output folder.
        """
        image_path = data["data"]["image"]
        annotations = data["annotations"]

        draw_bbox_image(image_path, annotations, output_folder)

    def import_dataset(self):
        """
        Import the COCO dataset and generate the label_studio.json file.
        """
        label_studio_json = []

        for subset in ["train", "test", "valid", "."]:
            subset_folder = os.path.join(self.source_folder, subset)

            try:
                with open(
                    os.path.join(subset_folder, "_annotations.coco.json"), "r"
                ) as coco_file:
                    coco_data = json.load(coco_file)
            except FileNotFoundError:
                logger.info(
                    f'Annotation file not found in: "{subset_folder}" . Skipping...'
                )
                continue

            logger.info(
                f"Processing dataset from: \"{subset_folder}\" . Number of images: {len(coco_data['images'])}"
            )

            for image_info in coco_data["images"]:
                image_id = image_info["id"]
                file_name = image_info["file_name"]
                height = image_info["height"]
                width = image_info["width"]
                target_image_path = os.path.join(self.files_folder, file_name)

                try:
                    # Copy image file to files folder
                    shutil.copy2(
                        os.path.join(subset_folder, file_name), target_image_path
                    )
                except FileNotFoundError:
                    logger.warning(f"Image file not found: {file_name}.")

                annotations = []

                for annotation in coco_data["annotations"]:
                    if annotation["image_id"] == image_id:
                        category_id = annotation["category_id"]
                        bbox = annotation["bbox"]
                        label = self.get_category_name(coco_data, category_id)

                        annotation_item = {
                            "type": "rectanglelabels",
                            "original_width": width,
                            "original_height": height,
                            "image_rotation": 0,
                            "value": {
                                "x": bbox[0] / width * 100,
                                "y": bbox[1] / height * 100,
                                "width": bbox[2] / width * 100,
                                "height": bbox[3] / height * 100,
                                "rotation": 0,
                                "rectanglelabels": [label],
                            },
                        }
                        annotations.append(annotation_item)

                label_studio_item = {
                    "data": {
                        "image": os.path.relpath(target_image_path, self.output_folder),
                        "annotations": annotations,
                    },
                }

                label_studio_json.append(label_studio_item)

        output_file = os.path.join(self.output_folder, "dataset.json")
        with open(output_file, "w") as f:
            json.dump(label_studio_json, f, indent=4)

        self.generate_metadata(label_studio_json)

    def get_category_name(self, coco_data, category_id):
        """
        Get the category name based on category_id.

        Args:
            coco_data (dict): The COCO dataset dictionary.
            category_id (int): The category_id to look up.

        Returns:
            str: The category name.
        """
        for category in coco_data["categories"]:
            if category["id"] == category_id:
                return category["name"]
        return "unknown"

    def generate_metadata(self, data):
        """
        Generate the metadata of the dataset.

        Args:
            data (list): The dataset as an array of objects.
        """
        labels = set()
        for item in data:
            for annotation in item["data"]["annotations"]:
                for label in annotation["value"]["rectanglelabels"]:
                    labels.add(label)

        labels_mapping = generate_labels_mapping(labels)
        labels_mapping_file = os.path.join(self.output_folder, "metadata.json")
        with open(labels_mapping_file, "w") as f:
            json.dump(labels_mapping, f, indent=4)

    def get_input_action_types(self):
        """
        Get the input and action types of the dataset.

        Returns:
            tuple: The input and action types.
        """
        return "IMAGE", "IMAGE_OBJECT_DETECTION"
