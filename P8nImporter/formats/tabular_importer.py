import pandas as pd
import os
import json

from ..config.logging import logger
from ..formats.base_importer import BaseImporter


class TabularImporter(BaseImporter):
    def __init__(self, root_folder, output_folder):
        """
        Initialize the TabularImporter class.

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
        Imports the dataset from CSV, Excel, or Parquet files and saves it as Parquet.

        This method supports both single file and multiple files in a folder.

        Raises:
            Exception: If the schemas of the files are not consistent.
        """
        dataframes = []

        if os.path.isdir(self.source_folder):
            all_files = [
                f
                for f in os.listdir(self.source_folder)
                if f.endswith((".csv", ".xlsx", ".parquet"))
            ]
            files_to_process = [os.path.join(self.source_folder, f) for f in all_files]
        elif os.path.isfile(self.source_folder):
            files_to_process = [self.source_folder]
        else:
            raise FileNotFoundError(
                f"No file or directory found at {self.source_folder}"
            )

        schema = None

        for file_path in files_to_process:
            logger.info(f"Processing file: {file_path}")
            if file_path.endswith(".csv"):
                df = pd.read_csv(file_path)
            elif file_path.endswith(".xlsx"):
                df = pd.read_excel(file_path)
            else:  # .parquet
                df = pd.read_parquet(file_path)

            if schema is None:
                schema = df.columns
            elif not all(schema == df.columns):
                raise Exception(f"Schema mismatch in file: {file_path}")

            dataframes.append(df)

        combined_df = pd.concat(dataframes, ignore_index=True)
        combined_df_path = os.path.join(self.files_folder, "dataset.parquet")
        combined_df.to_parquet(combined_df_path)

        # generate label studio json
        label_studio_json = [
            {
                "data": {"file": os.path.relpath(combined_df_path, self.output_folder),"annotations": []},
            }
        ]

        output_file = os.path.join(self.output_folder, "dataset.json")
        with open(output_file, "w") as f:
            json.dump(label_studio_json, f, indent=4)

        logger.info(f"Dataset saved at: {combined_df_path}")

        self.generate_metadata(combined_df)

    def generate_metadata(self, data):
        """
        Generates metadata for the dataset and saves it as metadata.json.

        Args:
            data (DataFrame): The dataframe for which metadata is generated.
        """
        columns = list(data.columns)
        print("Columns in the dataset:")
        for index, column in enumerate(columns):
            print(f"{index + 1}. {column}")

        target_column_index = input("Enter the index number of the target column: ")

        # Validate the user input
        if not target_column_index.isdigit():
            raise ValueError("Invalid index for the target column.")

        target_column_index = int(target_column_index) - 1  # Adjust for zero-based indexing

        if target_column_index < 0 or target_column_index >= len(columns):
            raise ValueError("Invalid target column index.")

        metadata = {"target": columns[target_column_index]}
        metadata_file = os.path.join(self.output_folder, "metadata.json")
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=4)


    def get_input_action_types(self):
        """
        Get the input and action types of the dataset.

        Returns:
            tuple: The input and action types.
        """
        return "TABULAR", "TABULAR_CLASSIFICATION,TABULAR_REGRESSION"
