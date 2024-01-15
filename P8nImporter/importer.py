import os
import tempfile
from .uploader import upload_dataset
from .utilities.importer import setup_importer

class P8nImporter:
    def __init__(self, api_key=None, dataset_id=None, format=None):
        if format:
            self.format = format.lower()
        self.api_key = api_key
        self.output_folder = tempfile.TemporaryDirectory()

        if dataset_id:
            self.dataset_id = dataset_id

        if api_key:
            self.api_key = api_key
        else:
            if os.environ.get("PROPULSIONAI_API_KEY"):
                self.api_key = os.environ.get("PROPULSIONAI_API_KEY")
            else:
                raise ValueError("API key is required")

    def import_dataset(self, source_folder, format, dataset_id=None):
        self.source_folder = source_folder
        
        # Set dataset_id if it is not None
        if dataset_id:
            self.dataset_id = dataset_id
        else:
            if not self.dataset_id:
                self.cleanup()
                raise ValueError("Dataset ID is required")
            
        if format:
            self.format = format.lower()
            self.importer = setup_importer(format, self.source_folder, self.output_folder)
        else:
            self.cleanup()
            raise ValueError("Format is required")
        
        try:
            self.importer.import_dataset()
            upload_dataset(self.output_folder, self.dataset_id, self.api_key)
        finally:
            self.cleanup()

    def import_task(self, format=None, dataset_id=None, **kwargs):
        if dataset_id:
            self.dataset_id = dataset_id
        else:
            if not self.dataset_id:
                self.cleanup()
                raise ValueError("Dataset ID is required")
        
        if format:
            self.format = format.lower()
            self.source_folder = tempfile.TemporaryDirectory()
            self.importer = setup_importer(format, self.source_folder.name, self.output_folder.name)
        else:
            self.cleanup()
            raise ValueError("Format is required")
            
            
        try:
            self.importer.import_task(**kwargs)
            upload_dataset(self.output_folder.name, self.dataset_id, self.api_key)
        finally:
            self.cleanup()

    def cleanup(self):
        if self.output_folder:
            self.output_folder.cleanup()
