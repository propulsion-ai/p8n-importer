import json
import os
import shutil
import yaml

from src.formats.base_importer import BaseImporter
from src.config.logging import logger
from src.utilities.visualize import draw_bbox_image

class YOLOv8Importer(BaseImporter):
    def __init__(self, annotations_path, output_folder):
        """
        Initialize YOLOv8Importer object.

        Args:
            annotations_path (str): Path to the folder having data.yaml file.
            output_folder (str): Path to the output folder where the label_studio.json file will be saved.
        """
        super().__init__(annotations_path, output_folder)
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
        Import the YOLOv8 dataset and generate the label_studio.json file.
        """
        label_studio_json = []

        with open(os.path.join(self.source_folder, "data.yaml"), 'r') as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)

        label_names = yaml_data['names']
        num_classes = len(label_names)

        if 'path' in yaml_data and yaml_data['path']:
            root_folder = yaml_data['path']
        else:
            root_folder = self.source_folder

        folders = []

        train_folder = yaml_data['train']

        if train_folder.startswith('../'):
            train_folder = train_folder[3:]

        if train_folder and os.path.exists(os.path.join(root_folder, train_folder)):
            folders.append(os.path.split(os.path.join(root_folder, train_folder))[0])
        else:
            logger.error(f"Train folder not found: {train_folder}")
            raise FileNotFoundError

        val_folder = yaml_data['val']

        if val_folder.startswith('../'):
            val_folder = val_folder[3:]

        if val_folder and os.path.exists(os.path.join(root_folder, val_folder)):
            folders.append(os.path.split(os.path.join(root_folder, val_folder))[0])
        else:
            logger.error(f"Validation folder not found: {val_folder}")
        
        test_folder = yaml_data['test']

        if test_folder.startswith('../'):
            test_folder = test_folder[3:]

        if test_folder and os.path.exists(os.path.join(root_folder, test_folder)):
            folders.append(os.path.split(os.path.join(root_folder, test_folder))[0])
        else:
            logger.error(f"Test folder not found: {test_folder}")

        for subset in folders:
            images_folder = os.path.join(subset, "images")
            labels_folder = os.path.join(subset, "labels")

            label_files = os.listdir(labels_folder)

            for label_file in label_files:
                image_file = os.path.splitext(label_file)[0] + ".jpg"
                image_path = os.path.join(images_folder, image_file)
                label_path = os.path.join(labels_folder, label_file)

                print(image_path, label_path)

                if os.path.exists(image_path) and os.path.exists(label_path):
                    # Copy image file to files folder
                    target_image_path = os.path.join(self.files_folder, image_file)

                    try:
                        shutil.copy2(image_path, target_image_path)
                    except FileNotFoundError:
                        logger.error(f"Image file not found: {image_path}")
                        raise

                    annotations = []

                    with open(label_path, 'r') as label_file:
                        lines = label_file.readlines()
                        for line in lines:
                            line = line.strip().split()
                            if len(line) == 5:  # Expected YOLO label format (class_id, x_center, y_center, width, height)
                                class_id, x_center, y_center, width, height = map(float, line)
                                label = label_names[int(class_id)]

                                x_center *= 100  # Convert to percentage
                                y_center *= 100
                                width *= 100
                                height *= 100

                                # Calculate top-left coordinates
                                x = x_center - width / 2
                                y = y_center - height / 2


                                annotation_item = {
                                    'type': 'rectanglelabels',
                                    'value': {
                                        'x': x,
                                        'y': y,
                                        'width': width,
                                        'height': height,
                                        'rectanglelabels': [label]
                                    }
                                }
                                annotations.append(annotation_item)
                            else:
                                logger.warning(f"Invalid label format: {line}, skipping...")
                                continue
                    label_studio_item = {
                        'data': {
                            'image': os.path.relpath(target_image_path, self.output_folder)
                        },
                        'annotations': annotations
                    }

                    label_studio_json.append(label_studio_item)
                else:
                    logger.warning(f"Image file or label file not found: {image_path} / {label_path}, skipping...")

        output_file = os.path.join(self.output_folder, 'dataset.json')
        with open(output_file, 'w') as f:
            json.dump(label_studio_json, f, indent=4)
