import json
import os
import csv
import shutil
import pandas as pd

from ..config.logging import logger
from .base_importer import BaseImporter
from ..utilities import generate_random_id


class ASRImporter(BaseImporter):
    def __init__(self, root_folder, output_folder):
        super().__init__(root_folder, output_folder)
        self.files_folder = os.path.join(self.output_folder, "files")
        if not os.path.exists(self.files_folder):
            os.makedirs(self.files_folder)

    def import_dataset(self):
        label_studio_json = []

        # Raise exception if self.source_folder is a directory
        if os.path.isdir(self.source_folder):
            raise Exception("The source must be a csv file.")

        try:
            df = pd.read_csv(self.source_folder, header=0, encoding="utf-8")
        except Exception as e:
            logger.error(f"Error reading the file {self.source_folder}. {e}")
            raise e

        # check if the csv has columns filename/file_name and text
        if len(df.columns) < 2:
            raise Exception("The csv file must have at least 2 columns.")

        if "file_name" in df.columns:
            df.rename(columns={"file_name": "filename"}, inplace=True)
        elif "file" in df.columns:
            df.rename(columns={"file": "filename"}, inplace=True)
        elif "filename" not in df.columns:
            raise Exception(
                "The csv file must have a column named filename or file_name or file."
            )

        if "text" not in df.columns:
            raise Exception("The csv file must have a column named text.")

        # remove nan values from the dataframe
        df = df.dropna(subset=["filename", "text"])

        for index, row in df.iterrows():
            parent_directory = os.path.dirname(self.source_folder)
            audio_path = row["filename"]
            text = row["text"]
            print("paths", parent_directory, audio_path, text)
            audio_path = os.path.join(parent_directory, audio_path)
            audio_file = os.path.basename(audio_path)
            target_image_path = os.path.join(self.files_folder, audio_file)

            try:
                shutil.copy(audio_path, target_image_path)
            except Exception as e:
                logger.error(f"Error copying the file {audio_path}. {e}")
                raise e

            id = generate_random_id()

            label_studio_json.append(
                {
                    "data": {
                        "audio": audio_file,
                        "annotations": [
                            {
                                "value": {"text": [text]},
                                "id": id,
                                "from_name": "transcription",
                                "to_name": "audio",
                                "type": "textarea",
                            }
                        ],
                    }
                }
            )

        # save the json to a file
        output_file = os.path.join(self.output_folder, "dataset.json")
        with open(output_file, "w") as f:
            json.dump(label_studio_json, f, indent=4)

    def get_input_action_types(self):
        """
        Get the input and action types of the dataset.

        Returns:
            tuple: The input and action types.
        """
        return "AUDIO", "AUDIO_TRANSCRIPTION"
