# src/cli.py
import argparse
import logging
import os
import shutil
import tempfile
from getpass import getpass

from src.config.logging import setup_logger
from src.formats.coco_json_importer import COCOImporter
from src.formats.voc_importer import VOCImporter
from src.formats.yolov8_importer import YOLOv8Importer
from src.uploader import upload_dataset
from src.utilities.file import load_json
from src.utilities.visualize import visualize_dataset


def get_api_key():
    api_key = os.environ.get("PROPULSIONAI_API_KEY")
    if not api_key:
        print("API key not found in environment variables.")
        api_key = getpass("Please enter your API key: ")
        if not api_key:
            raise ValueError("API key cannot be blank.")
    return api_key

def get_dataset_id():
    dataset_id = input("Please enter the Dataset ID: ")
    if not dataset_id:
        raise ValueError("Dataset ID cannot be blank.")
    return dataset_id
    
    # Uncomment below to enable new dataset creation
    """
    if not dataset_id:
        name = input("Enter the name for the new dataset: ")
        description = input("Enter a description for the new dataset: ")
        input_type = input("Enter the input type for the new dataset: ")
        action_type = input("Enter the action type for the new dataset: ")
        # API call to create new dataset and retrieve dataset_id
        # dataset_id = create_new_dataset(api_key, name, description, input_type, action_type)
    """

def visualize(json_data, output_folder):
    while True:
        try:
            json_index = input("Enter a number between 0 and {} to visualize (or type 'skip' to proceed with upload): ".format(len(json_data) - 1))
            if json_index.lower() == 'skip':
                break

            json_index = int(json_index)
            if 0 <= json_index < len(json_data):
                visualize_dataset(json_data[json_index], output_folder)
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

    api_key = get_api_key()
    dataset_id = get_dataset_id()

    with tempfile.TemporaryDirectory() as temp_output_folder:
        if args.format.lower() == 'voc':
            importer = VOCImporter(args.source_folder, temp_output_folder)
        elif args.format.lower() == 'coco_json':
            importer = COCOImporter(args.source_folder, temp_output_folder)
        elif args.format.lower() == 'yolov8':
            importer = YOLOv8Importer(args.source_folder, temp_output_folder)
        # Add other format conditions here
        else:
            raise ValueError("Unsupported format")

        importer.import_dataset()

        if args.visualize:
            print("Visualizing converted dataset...")
            json_data = load_json(os.path.join(temp_output_folder, 'dataset.json'))
            visualize(json_data, temp_output_folder)
        
        if args.no_upload:
            print("Saving converted dataset...")
            output_folder = "conversion_output"  # Specify the name of the output folder
            # Create the output folder if it doesn't exist
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # Copy the contents of temp_output_folder to the output folder
            shutil.copytree(temp_output_folder, os.path.join(output_folder, os.path.basename(temp_output_folder)))
        else:
            upload_dataset(temp_output_folder, dataset_id, api_key)

if __name__ == "__main__":
    main()
