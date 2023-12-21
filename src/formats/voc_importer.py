import json
import os
import shutil
import xml.etree.ElementTree as ET

from src.formats.base_importer import BaseImporter
from src.utilities.file import find_file
from src.config.logging import logger


class VOCImporter(BaseImporter):
    def __init__(self, annotations_path, output_folder):
        """
        Initialize VOCImporter object.

        Args:
            annotations_path (str): Path to the folder containing VOC annotation files.
            output_folder (str): Path to the output folder where the label_studio.json file will be saved.
        """
        super().__init__(annotations_path, output_folder)
        self.files_folder = os.path.join(self.output_folder, "files")
        if not os.path.exists(self.files_folder):
            os.makedirs(self.files_folder)

    def import_dataset(self):
        """
        Import the VOC dataset and generate the label_studio.json file.
        """
        label_studio_json = []

        for annotation_file in os.listdir(self.source_folder):
            if annotation_file.endswith('.xml'):
                logger.info(f"Processing annotation file: {annotation_file}")

                tree = ET.parse(os.path.join(self.source_folder, annotation_file))
                root = tree.getroot()

                image_path = root.find('path').text
                image_file = os.path.basename(image_path)
                target_image_path = os.path.join(self.files_folder, image_file)

                try:
                    # Copy image file to files folder
                    shutil.copy2(image_path, target_image_path)
                except FileNotFoundError:
                    logger.warning(f"Image file not found: {image_path} Searching alternative paths...")
                    new_path = find_file(image_path, self.source_folder)
                    if new_path:
                        try:
                            shutil.copy2(new_path, target_image_path)
                            logger.info(f"File found in alternative path: {new_path}.")
                        except FileNotFoundError:
                            logger.error(f"File not found in alternative path: {new_path}.")
                            raise
                    else:
                        logger.error(f"File not found in alternative path.")
                        raise

                width = int(root.find('size/width').text)
                height = int(root.find('size/height').text)

                annotations = []

                for obj in root.findall('object'):
                    label = obj.find('name').text
                    bndbox = obj.find('bndbox')
                    xmin = int(bndbox.find('xmin').text)
                    ymin = int(bndbox.find('ymin').text)
                    xmax = int(bndbox.find('xmax').text)
                    ymax = int(bndbox.find('ymax').text)

                    annotation = {
                        'type': 'rectanglelabels',
                        'original_width': width,
                        'original_height': height,
                        'image_rotation': 0,
                        'value': {
                            'x': 100 * xmin / width,
                            'y': 100 * ymin / height,
                            'width': 100 * (xmax - xmin) / width,
                            'height': 100 * (ymax - ymin) / height,
                            'rotation': 0,
                            'rectanglelabels': [label]
                        }
                    }
                    annotations.append(annotation)

                label_studio_item = {
                    'data': {
                        'image': os.path.relpath(target_image_path, self.output_folder)
                    },
                    'annotations': annotations
                }

                label_studio_json.append(label_studio_item)

        output_file = os.path.join(self.output_folder, 'dataset.json')
        with open(output_file, 'w') as f:
            json.dump(label_studio_json, f, indent=4)
