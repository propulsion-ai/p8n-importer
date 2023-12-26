# This file contains the BaseImporter class.

class BaseImporter:
    def __init__(self, source_folder, output_folder):
        """
        Initializes a BaseImporter object.

        Args:
            source_folder (str): The path to the source folder.
            output_folder (str): The path to the output folder.
        """
        self.source_folder = source_folder
        self.output_folder = output_folder

    def import_dataset(self):
        """
        Imports the dataset.

        This method should be overridden in a subclass.
        """
        raise NotImplementedError("This method should be overridden in a subclass")
    
    def visualize(self, data, output_folder):
        """
        Visualizes the dataset.

        This method should be overridden in a subclass.
        """
        raise NotImplementedError("This method should be overridden in a subclass")
    
    def generate_metadata(self, data):
        """
        Generates the metadata of the dataset.

        This method should be overridden in a subclass.
        """
        raise NotImplementedError("This method should be overridden in a subclass")
        