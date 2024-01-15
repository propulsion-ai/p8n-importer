# .cli.py
import argparse
import logging
import os
import shutil
import tempfile
from getpass import getpass

from .api.datasets import create_dataset
from .config.logging import setup_logger
from .formats import (BaseImporter, COCOImporter,
                         ImageClassificationImporter, TabularImporter,
                         VOCImporter, YOLOv8Importer)
from .uploader import upload_dataset
from .utilities.file import load_json
from .utilities.keys import get_project_id


def get_api_key():
    api_key = os.environ.get("PROPULSIONAI_API_KEY")
    if not api_key:
        print("API key not found in environment variables.")
        api_key = getpass("Please enter your API key: ")
        if not api_key:
            raise ValueError("API key cannot be blank.")
    return api_key


def get_dataset_id(importer: BaseImporter, api_key: str):
    dataset_id = input("Please enter the Dataset ID (skip to create a new dataset): ")

    if not dataset_id:
        project_id = get_project_id(api_key)

        name = input("Enter the name for the new dataset: ")

        if not name:
            raise ValueError("Dataset name cannot be blank.")

        description = input("Enter a description for the new dataset: ")

        if not description:
            raise ValueError("Dataset description cannot be blank.")

        default_input_type, default_action_type = importer.get_input_action_types()

        input_type = input(
            f"Enter the input type for the new dataset (suggested: {default_input_type}): "
        )

        if not input_type.strip():
            input_type = default_input_type

        if default_action_type and default_action_type != "None":
            if len(default_action_type.split(",")) > 1:
                options = default_action_type.split(",")
                print("Please select one of the following action types:")
                for i, option in enumerate(options):
                    print(f"{i}: {option}")
                action_type_index = input("Enter the index of the action type: ")   
                if not action_type_index.isdigit():
                    raise ValueError("Invalid index for the action type.")

                action_type = options[int(action_type_index)]
            else:
                action_type = input(
                    f"Enter the action type for the new dataset (suggested: {default_action_type}): "
                )

                if not action_type.strip():
                    action_type = default_action_type
        else:
            action_type = input(f"Enter the action type for the new dataset: ")
            if not action_type:
                raise ValueError("Action type cannot be blank.")

        # API call to create new dataset and retrieve dataset_id
        dataset_id = create_dataset(
            name, description, project_id, input_type, action_type, api_key
        ).json()["dataset"]["id"]

        print(f"Created new dataset with ID: {dataset_id}.")

        return dataset_id
    else:
        # check valid dataset_id
        try:
            int(dataset_id)
            return dataset_id
        except ValueError:
            raise ValueError("Dataset ID should be an integer.")


def visualize(importer, json_data, output_folder):
    while True:
        try:
            json_index = input(
                "Enter a number between 0 and {} to visualize (or type 'skip' to proceed with upload): ".format(
                    len(json_data) - 1
                )
            )
            if json_index.lower() == "skip":
                break

            json_index = int(json_index)
            if 0 <= json_index < len(json_data):
                importer.visualize(json_data[json_index], output_folder)
            else:
                print("Invalid number. Please try again.")

        except ValueError:
            print("Invalid input. Please enter a valid number or 'skip'.")


def main():
    print("Welcome to the PropulsionAI Dataset Importer!")
    print("This tool will help you import datasets into the PropulsionAI platform.\n")

    parser = argparse.ArgumentParser(description="PropulsionAI Dataset Importer")
    parser.add_argument("format", help="Dataset format (e.g., 'voc', 'yolov8', 'coco_json')")
    parser.add_argument("source_folder", help="Path to the source dataset folder")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--no-upload", action="store_true", help="Skip uploading the converted dataset to the platform")
    parser.add_argument("--visualize", action="store_true", help="Visualize the converted dataset before uploading")

    args = parser.parse_args()

    # Set logger level based on verbose flag
    if args.verbose:
        setup_logger(level=logging.INFO)
    else:
        setup_logger(level=logging.WARNING)

    with tempfile.TemporaryDirectory() as temp_output_folder:
        if args.format.lower() == "voc":
            importer = VOCImporter(args.source_folder, temp_output_folder)
        elif args.format.lower() == "coco_json":
            importer = COCOImporter(args.source_folder, temp_output_folder)
        elif args.format.lower() == "yolov8":
            importer = YOLOv8Importer(args.source_folder, temp_output_folder)
        elif args.format.lower() == "im_classification":
            importer = ImageClassificationImporter(args.source_folder, temp_output_folder)
        elif args.format.lower() == "tabular":
            importer = TabularImporter(args.source_folder, temp_output_folder)
        else:
            raise ValueError("Unsupported format")

        # Get API key and dataset ID
        api_key = get_api_key()
        dataset_id = get_dataset_id(importer, api_key)

        importer.import_dataset()

        if args.visualize:
            print("Visualizing converted dataset...")
            json_data = load_json(os.path.join(temp_output_folder, "dataset.json"))
            visualize(importer, json_data, temp_output_folder)

        if args.no_upload:
            output_folder = (
                "p8n_conversion_output"  # Specify the name of the output folder
            )
            # Create the output folder if it doesn't exist
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            # Copy the contents of temp_output_folder to the output folder
            shutil.copytree(
                temp_output_folder,
                os.path.join(output_folder, os.path.basename(temp_output_folder)),
            )

            print(
                f"Saved converted dataset to {output_folder}/{os.path.basename(temp_output_folder)}."
            )
        else:
            upload_dataset(temp_output_folder, dataset_id, api_key)


if __name__ == "__main__":
    main()
