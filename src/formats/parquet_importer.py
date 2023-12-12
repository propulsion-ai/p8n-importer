import os
import json
import pyarrow.parquet as pq
from src.formats.base_importer import BaseImporter

class ParquetImporter(BaseImporter):
    def __init__(self, annotations_path, output_folder):
        """
        Initialize ParquetImporter object.

        Args:
            annotations_path (str): Path to the folder containing Parquet annotation files.
            output_folder (str): Path to the output folder where the dataset.jsonl file will be saved.
        """
        super().__init__(annotations_path, output_folder)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    def import_dataset(self):
        """
        Import the Parquet dataset and generate the dataset.jsonl file.
        """
        pds = pq.read_pandas(self.source_folder, columns=None).to_pandas()
        pds.dropna(inplace=True)
        output_file = os.path.join(self.output_folder, 'dataset.jsonl')
        pds.to_json(path_or_buf=output_file, orient='records', lines=True, date_format='iso', date_unit='us')
        
        output_file = os.path.join(self.output_folder, 'dataset.jsonl')
        with open(output_file, 'w', encoding='utf-8') as file:
            for _, row in pds.iterrows():
                # Assuming the conversation is in a column named 'text'
                conversation = row['text'].split('\n')
                entry = {}

                for line in conversation:
                    if line.startswith('<HUMAN>:'):
                        entry['human'] = line.replace('<HUMAN>:', '').strip()
                    elif line.startswith('<ASSISTANT>:'):
                        entry['assistant'] = line.replace('<ASSISTANT>:', '').strip()

                # Write the entry as a JSON line if it's not empty
                if entry:
                    file.write(json.dumps(entry, ensure_ascii=False) + '\n')